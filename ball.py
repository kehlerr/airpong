import pygame
import math

from collections import deque
from random import randint
from numpy import sign

from round_object import RoundObject
from ball_collision import CollisionWithVBorder, CollisionWithHBorder,\
            CollisionWithGoal, CollisionWithRound, CollisionWithSlider
from sparkles import Sparkles

BALL_RAD = 20
BALL_SPEED = 10
MAX_BALL_SPEED = 35
ZERO_MOVES_COUNT_MAX=5

MIN_SPARKLES_AMOUNT = 60
MAX_SPARKLES_AMOUNT = 80


class Ball(RoundObject):
    size = (BALL_RAD, BALL_RAD)
    image_path = 'pic/ball_blue.png'
    start_speed = BALL_SPEED
    radius = BALL_RAD/2

    def __init__(
            self, background_surface, pos, group, collision_objects, thread,
            image_path = None,
            size = None,
            angle = None
        ):
        super(Ball, self).__init__(
            background_surface, pos, image_path, group, size, angle
        )
        self.thread = thread
        self.angle = self.get_random_angle()
        self.dang = 0
        self.rotation = 0
        self.zero_dx_count = ZERO_MOVES_COUNT_MAX
        self.zero_dy_count = 0
        self.speed = self.start_speed
        self.collision = None
        self.fill_collision_objects(collision_objects)
        self.prepare_sparkles()

    def reset(self):
        self.speed = self.start_speed
        self.dang = 0
        self.rotation = 0

    def fill_collision_objects(self, collision_objects):
        self.sliders = collision_objects.get('sliders', [])
        self.posts = collision_objects.get('posts', [])
        self.goals = collision_objects.get('goals', [])
        self.balls = list(collision_objects.get('balls', []))

    def get_round_collision_objects(self):
        return [*self.posts, *self.balls]

    def prepare_sparkles(self):
        self.sparkles_slider = Sparkles(
            self.background_surface, self.thread, group = self.group
        )
        self.sparkles_post = Sparkles(
            self.background_surface, self.thread,
            'pic/sparkle_post.png', self.group
        )

    def update(self):
        self.calculate_move()
        self.check_collision()
        if self.collision:
            self.collision.handle()
            self.process_moves_history()
            self.collision = None
        else:
            self.move(self.dx, self.dy)

    def process_moves_history(self):
        if self.dx == 0:
            self.zero_dx_count += 1
            if self.zero_dx_count >= ZERO_MOVES_COUNT_MAX:
                self.zero_dx_count = 0
                self.zero_dy_count = 0
                self.change_angle_slightly()
        else:
            if self.dy == 0:
                self.zero_dy_count += 1
                if self.zero_dy_count >= ZERO_MOVES_COUNT_MAX:
                    self.zero_dx_count = 0
                    self.zero_dy_count = 0
                    self.change_angle_slightly()
            else:
                self.zero_dy_count = 0

    def change_angle_slightly(self):
        self.dang = 0.003
        self.rotation = 0.08

    def calculate_move(self):
        self.dx = math.trunc(self.speed * math.cos(self.angle))
        self.dy = math.trunc(self.speed * math.sin(self.angle))
        if self.rotation > 0:
            self.angle += self.rotation
            self.rotation -= 0.01

    def check_collision(self):
        if CollisionWithHBorder.check(self):
            self.collision = CollisionWithHBorder(self)
            return

        if CollisionWithGoal.is_between_posts(self):
            if CollisionWithGoal.check(self):
                self.collision = CollisionWithGoal(self)
                return
        elif CollisionWithVBorder.check(self):
            self.collision = CollisionWithVBorder(self)
            return

        collision_round_object = CollisionWithRound.get_collision_object(self)
        if collision_round_object:
            self.collision = CollisionWithRound(self, collision_round_object)
            return

        collision_slider = CollisionWithSlider.get_collision_slider(self)
        if collision_slider:
            self.collision = CollisionWithSlider(self, collision_slider)
            return

    def generate_sparkles(self, sparkles_group):
        sparkles_count = randint(MIN_SPARKLES_AMOUNT, MAX_SPARKLES_AMOUNT)
        sparkles_group.generate_sparkles(sparkles_count, self.rect.center)
