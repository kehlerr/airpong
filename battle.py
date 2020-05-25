#!/usr/bin/python

from pygame.locals import *

from ball import *
from field import *
from scoreboard import *
from slider import *
from common import *
from thread_mgr import *

from phys_defs import UP, DOWN


PUTTING_BALL_WAIT = 500
ONSTART_PUTTING_BALL_WAIT = 2000
EV_MODIFY_BATTLE = pygame.USEREVENT + 1
EV_CLEAR_MODIFICATIONS = EV_MODIFY_BATTLE + 1
EV_PUT_BALL = pygame.USEREVENT + 3


class Battle:
    def __init__(self, display):
        self.display = display
        self.scoreboard = ScoreBoard('pic/scoreboard.png', (200, 600), (900, 300), self.display)
        self.thread = Thread()
        self.field = Field(self.display)
        self.score = (0, 0)
        self.update_score()
        self.sprites = pygame.sprite.RenderPlain()
        self.u_slider = Slider('pic/slider_red.png', (SLIDER_W, SLIDER_H), (L_GOAL_LINE + SLIDER_DISTX, self.field.rect.centery), self.sprites)
        self.b_slider = Slider('pic/slider_blue.png', (SLIDER_W, SLIDER_H), (R_GOAL_LINE - SLIDER_DISTX, self.field.rect.centery), self.sprites)
        self.sliders = [self.u_slider, self.b_slider]
        self.main_ball = Ball('pic/ball_blue.png', self.field.field_sfce, self.field.rect.center, self.thread, self.sprites)
        self.balls = [self.main_ball]
        self.additional_balls = []
        self.control_accel = 1
        self.state = 'need_wait_put_ball'
        self.modified = False
        pygame.time.set_timer(EV_MODIFY_BATTLE, 7000)
        pygame.time.set_timer(EV_PUT_BALL, 1500)

    def update(self, loop, ticks):
        for sprite in self.sprites:
            self.display.blit(self.field.field_sfce, sprite.rect, sprite.rect)

        loop()
        self.thread.update(ticks)

        if self.check_state('play'):
            self.process_balls()
        elif self.check_state('need_wait_put_ball'):
            self.update_state('waiting_put_ball')
            pygame.time.set_timer(EV_PUT_BALL, 500)
        for sprite in self.sprites:
            self.display.blit(sprite.image, sprite.rect)

        pygame.display.update(self.field.rect)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            is_pressed = pygame.key.get_pressed()
            if self.control_accel < 15: self.control_accel += 0.75
            if is_pressed[K_w]: self.u_slider.move(UP, self.control_accel)
            if is_pressed[K_s]: self.u_slider.move(DOWN, self.control_accel)
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
                self.update_state('need_wait_put_ball')
                self.clear_modifications()
        elif event.type == EV_MODIFY_BATTLE:
            self.modify()
        elif event.type == EV_CLEAR_MODIFICATIONS:
            self.clear_modifications()
        elif event.type == EV_PUT_BALL:
            self.update_state('play')
            pygame.time.set_timer(EV_PUT_BALL, 0)

    def update_score(self, d_score=None):
        if d_score:
            self.score = (self.score[0] + d_score[0], self.score[1] + d_score[1])
        self.scoreboard.set_score(self.score)
        pygame.display.update(self.scoreboard.rect)

    def update_state(self, state):
        self.state = state

    def check_state(self, state):
        return self.state == state

    def process_balls(self):
        for ball in self.balls:
            ball.update(self.sliders, self.field.posts.sprites(), self.field.goals.sprites(), self.balls)
        return True

    def modify(self):
        if not self.modified:
            self.modified = True
            pygame.time.set_timer(EV_CLEAR_MODIFICATIONS, 10000)
    
    def clear_modifications(self):
        if self.modified:
            for ball in self.balls[1:]:
                self.balls.remove(ball)
                ball.kill()
            self.modified = False
            pygame.time.set_timer(EV_CLEAR_MODIFICATIONS, 0)

    def add_ball_to_battle(self):
        self.balls.append(Ball('pic/ball_blue.png', self.field.field_sfce, self.field.rect.center, self.thread, self.sprites))

