#!/usr/bin/python

from pygame.locals import *
from field import *
from scoreboard import *
from slider import *
from ball import *


class Battle:
    def __init__(self, display):
        self.display = display
        self.scoreboard = ScoreBoard('pic/scoreboard.png', (200, 600), (900, 300), self.display)
        self.field = Field(self.display)
        self.score = (0, 0)
        self.update_score()
        self.balls = pygame.sprite.Group([])
        self.sliders = pygame.sprite.Group([])
        self.u_slider = Slider('pic/slider_red.png', (SLIDER_W, SLIDER_H), (L_GOAL_LINE + SLIDER_DISTX, 100), self.sliders)
        self.b_slider = Slider('pic/slider_blue.png', (SLIDER_W, SLIDER_H), (R_GOAL_LINE - SLIDER_DISTX, 100), self.sliders)
        Ball('pic/ball_blue.png', self.field.FieldSfce, (440,330), self.balls)
        self.sprites = pygame.sprite.RenderPlain(self.balls, self.sliders)
        self.control_accel = 1

    def update(self, loop):
        for sprite in self.sprites:
            self.display.blit(self.field.FieldSfce, sprite.rect, sprite.rect)

        loop()

        for sprite in self.sprites:
            self.display.blit(sprite.image, sprite.rect)

        pygame.display.update(self.field.rect)

    def play(self):
        for ball in self.balls:
            ball.Live(self.sliders.sprites(), self.field.posts.sprites(), self.field.goals.sprites())
            self.sprites.add(ball.sparkles)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            is_pressed = pygame.key.get_pressed()
            if self.control_accel < 15: self.control_accel += 0.75
            if is_pressed[K_w]: self.u_slider.Move(UP, self.control_accel)
            if is_pressed[K_s]: self.u_slider.Move(DOWN, self.control_accel)
# TODO [low] delete this in future
            if is_pressed[K_UP]: self.b_slider.Move(UP, self.control_accel)
            if is_pressed[K_DOWN]: self.b_slider.Move(DOWN, self.control_accel)
        elif event.type == KEYUP:
            self.control_accel = 1
        elif event.type == MOUSEMOTION:
            self.u_slider.Move(pygame.mouse.get_pos()[Y])
        elif event.type == USEREVENT:
            event_info = event.__dict__
            if 'collision' in event_info:
                if event_info['collision'] == WITH_GOAL_LEFT:
                    self.update_score((0, 1))
                if event_info['collision'] == WITH_GOAL_RIGHT:
                    self.update_score((1, 0))

    def update_score(self, d_score=None):
        if d_score:
            self.score = (self.score[0] + d_score[0], self.score[1] + d_score[1])
        self.scoreboard.set_score(self.score)
        pygame.display.update(self.scoreboard.rect)
