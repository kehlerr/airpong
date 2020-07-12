import math
from numpy import sign
import pygame

from common import X, Y
from field import FIELD_H, FIELD_W, L_GOAL_LINE, R_GOAL_LINE


MIN_SPARKLES_AMOUNT = 60
MAX_SPARKLES_AMOUNT = 80


class Collision:
    def __init__(self, ball):
        self.ball = ball

    def handle(self):
        self.change_angle()
        self.change_pos()

    def change_angle(self):
        raise NotImplementedError()

    def change_pos(self):
        raise NotImplementedError()

    @staticmethod
    def check():
        raise NotImplementedError()


class CollisionWithHBorder(Collision):
    def change_angle(self):
        self.ball.angle *= -1
        self.ball.dang = 0

    def change_pos(self):
        if self.ball.rect.top > FIELD_H/2:
            self.ball.rect.bottom = FIELD_H
        else:
            self.ball.rect.top = 0

    @staticmethod
    def check(ball):
        return ball.rect.top  < 0 or ball.rect.bottom > FIELD_H


class CollisionWithVBorder(Collision):
    def __init__(self, ball):
        super().__init__(ball)
        self.l_border_x = L_GOAL_LINE
        self.r_border_x = R_GOAL_LINE

    def change_angle(self):
        self.ball.angle = (math.pi - self.ball.angle)%(math.pi*2)
        self.ball.dang = 0

    def change_pos(self):
        if self.ball.rect.right > self.r_border_x:
            self.ball.rect.right = self.r_border_x
        elif self.ball.rect.left < self.l_border_x:
            self.ball.rect.left = self.l_border_x

    @staticmethod
    def check(ball):
        return ball.rect.left < L_GOAL_LINE or ball.rect.right > R_GOAL_LINE


class CollisionWithRound(Collision):
    def __init__(self, ball, round_object):
        self.ball = ball
        self.obj_x = round_object.rect.centerx
        self.obj_y = round_object.rect.centery
        self.obj_r = round_object.radius
        self.ang_collide = 0

    def define_ang_collide(self):
        dist_x = self.obj_x - self.ball.rect.centerx
        dist_y = self.obj_y - self.ball.rect.centery
        c_hypoten = math.hypot(dist_x, dist_y)
        h_cathet  = math.fabs(self.obj_y - self.ball.rect.centery)
        try:
            a = math.asin(h_cathet/c_hypoten)
            if self.ball.rect.centerx >= self.obj_x:
                self.ang_collide = a
            else: 
                self.ang_collide = math.pi-a
        except ValueError:
            self.ang_collide = 0

        if dist_y > 0:
            self.ang_collide *= -1

    def handle(self):
        self.define_ang_collide()
        super().handle()

    def change_angle(self):
        self.ball.angle = self.ang_collide
        self.ball.dang = 0

    def change_pos(self):
        r_sum = self.obj_r+self.ball.radius+5
        self.ball.rect.centerx = self.obj_x + \
            math.trunc(r_sum*math.cos(self.ang_collide))
        self.ball.rect.centery = self.obj_y + \
            math.trunc(r_sum*math.sin(self.ang_collide))

    @staticmethod
    def get_collision_object(ball):
        rounds = ball.get_round_collision_objects()
        for obj in rounds:
            dist_x = obj.rect.centerx - ball.rect.centerx
            dist_y = obj.rect.centery - ball.rect.centery
            if math.hypot(dist_x, dist_y) < (ball.radius + obj.radius):
                return obj
        return None

class CollisionWithGoal(CollisionWithVBorder):
    def handle(self):
        goal_side = self.ball.rect.centerx//(FIELD_W/2)
        ev = pygame.event.Event(pygame.USEREVENT,{'goal':goal_side})
        pygame.event.post(ev)
        self.change_pos()
        self.change_angle()
        self.ball.reset()

    def change_angle(self):
        self.ball.angle = self.ball.get_random_angle()

    def change_pos(self):
        self.ball.put()

    @staticmethod
    def is_between_posts(ball):
        goal = ball.goals[0]
        is_under_top_post = ball.rect.top > goal.rect.top
        if not is_under_top_post:
            return False

        is_above_bottom_post = ball.rect.bottom < goal.rect.bottom
        return is_above_bottom_post

    @staticmethod
    def check(ball):
        return ball.rect.right < L_GOAL_LINE or ball.rect.left > R_GOAL_LINE


class CollisionWithSlider(CollisionWithVBorder, CollisionWithRound):
    def __init__(self, ball, slider):
        Collision.__init__(self, ball)
        self.l_border_x = slider.rect.left
        self.r_border_x = slider.rect.right
        self.obj_x = slider.rect.centerx
        self.obj_r = slider.rect.width/2
        self.slider_yt = slider.rect.top + slider.width/2
        self.slider_yb = slider.rect.bottom - slider.width/2

    def handle(self):
        is_under_top_slider = self.ball.rect.centery > self.slider_yt
        is_above_bottom_slider = self.ball.rect.centery < self.slider_yb
        if is_under_top_slider and is_above_bottom_slider:
            self.change_pos_between_rounds()
            CollisionWithVBorder.change_angle(self)
        else:
            if is_above_bottom_slider:
                self.obj_y = self.slider_yt
            if is_under_top_slider:
                self.obj_y = self.slider_yb
            CollisionWithRound.handle(self)
        self.ball.dang = 0.00
        self.ball.generate_sparkles(self.ball.sparkles_slider)

    def change_pos_between_rounds(self):
        ball_offset_x = - sign(self.ball.dx)*(self.obj_r + self.ball.radius)
        self.ball.rect.centerx = self.obj_x + ball_offset_x

    def change_pos(self):
        CollisionWithRound.change_pos(self)

    def change_angle(self):
        CollisionWithRound.change_angle(self)

    @staticmethod
    def get_collision_slider(ball):
        for slider in ball.sliders:
            slider_xl = slider.rect.left
            slider_xr = slider.rect.right
            ball_xc = ball.rect.centerx

            if ((ball_xc < slider_xr and ball_xc > slider_xl or
                CollisionWithSlider.check_intersect(ball, slider)) and
                pygame.sprite.collide_mask(ball, slider)):
                return slider

    @staticmethod
    def check_intersect(ball, slider):
        def onSegment(a, b, c):
            return (
                a[X] <= max(b[X], c[X]) and a[X] >= min(b[X], c[X]) and
                a[Y] <= max(b[Y], c[Y]) and a[Y] >= min(b[Y], c[Y])
            )

        def CCW_orientation(a, b, c):
            val = (a[Y]-b[Y])*(c[X]-a[X])-(a[X]-b[X])*(c[Y]-a[Y])
            if val == 0:
                return 0
            elif val > 0:
                return 1
            else:
                return 2

        x1 = ball.rect.centerx
        y1 = ball.rect.centery
        ball_p1 = (x1,y1)

        x2 = ball.rect.centerx + ball.dx
        y2 = ball.rect.centery + ball.dy
        ball_p2 = (x2, y2)

        slider_rad = slider.rect.width/2

        x3 = slider.rect.centerx - sign(ball.dx)*slider_rad
        y3 = slider.rect.top + slider_rad
        slider_p1 = (x3, y3)

        x4 = x3
        y4 = slider.rect.bottom - slider_rad
        slider_p2 = (x4, y4)

        o1 = CCW_orientation(ball_p1, ball_p2, slider_p1)
        o2 = CCW_orientation(ball_p1, ball_p2, slider_p2)
        o3 = CCW_orientation(slider_p1, slider_p2, ball_p1)
        o4 = CCW_orientation(slider_p1, slider_p2, ball_p2)

        return (o1 != o2 and o3 != o4 or
            o1 == 0 and onSegment(ball_p1, slider_p1, ball_p2) or
            o2 == 0 and onSegment(ball_p1, slider_p2, ball_p2) or
            o3 == 0 and onSegment(slider_p1, ball_p1, slider_p2) or
            o4 == 0 and onSegment(slider_p1, ball_p2, slider_p2))