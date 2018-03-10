#!/usr/bin/python

from pygame.locals import *

from ball import *
from field import *
from scoreboard import *
from slider import *
from common import *

from phys_defs import UP, DOWN


PUTTING_BALL_WAIT = 500
ONSTART_PUTTING_BALL_WAIT = 5000

class Battle:
    def __init__(self, display):
        self.display = display
        self.scoreboard = ScoreBoard('pic/scoreboard.png', (200, 600), (900, 300), self.display)
        self.field = Field(self.display)
        self.score = (0, 0)
        self.update_score()
        self.balls = pygame.sprite.Group([])
        self.sliders = pygame.sprite.Group([])
        self.u_slider = Slider('pic/slider_red.png', (SLIDER_W, SLIDER_H), (L_GOAL_LINE + SLIDER_DISTX, self.field.rect.centery), self.sliders)
        self.b_slider = Slider('pic/slider_blue.png', (SLIDER_W, SLIDER_H), (R_GOAL_LINE - SLIDER_DISTX, self.field.rect.centery), self.sliders)
        Ball('pic/ball_blue.png', self.field.field_sfce, self.field.rect.center, self.balls)
        self.sprites = pygame.sprite.RenderPlain(self.balls, self.sliders)
        self.control_accel = 1
        self.wait_putting_ball = ONSTART_PUTTING_BALL_WAIT
        self.state = 'wait_putting_ball'

    def update(self, loop, ticks):
        for sprite in self.sprites:
            self.display.blit(self.field.field_sfce, sprite.rect, sprite.rect)

        loop()

        if self.check_state('play'):
            for ball in self.balls:
                ball.update(self.sliders.sprites(), self.field.posts.sprites(), self.field.goals.sprites())
                self.sprites.add(ball.sparkles)
        elif self.check_state('wait_putting_ball'):
            self.wait_putting_ball -= ticks
            if self.wait_putting_ball < 0:
                self.wait_putting_ball = PUTTING_BALL_WAIT
                self.update_state('play')

        for sprite in self.sprites:
            self.display.blit(sprite.image, sprite.rect)

        pygame.display.update(self.field.rect)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            is_pressed = pygame.key.get_pressed()
            if self.control_accel < 15: self.control_accel += 0.75
            if is_pressed[K_w]: self.u_slider.move(UP, self.control_accel)
            if is_pressed[K_s]: self.u_slider.move(DOWN, self.control_accel)
# TODO [low] delete this in future
            if is_pressed[K_UP]: self.b_slider.move(UP, self.control_accel)
            if is_pressed[K_DOWN]: self.b_slider.move(DOWN, self.control_accel)
        elif event.type == KEYUP:
            self.control_accel = 1
        elif event.type == MOUSEMOTION:
            self.u_slider.move(pygame.mouse.get_pos()[Y])
        elif event.type == USEREVENT:
            event_info = event.__dict__
            if 'collision' in event_info:
                if event_info['collision'] == WITH_GOAL_LEFT:
                    self.update_score((0, 1))
                if event_info['collision'] == WITH_GOAL_RIGHT:
                    self.update_score((1, 0))
                self.update_state('wait_putting_ball')

    def update_score(self, d_score=None):
        if d_score:
            self.score = (self.score[0] + d_score[0], self.score[1] + d_score[1])
        self.scoreboard.set_score(self.score)
        pygame.display.update(self.scoreboard.rect)

    def update_state(self, state):
        self.state = state

    def check_state(self, state):
        return self.state == state
