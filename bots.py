from math import fabs
from random import randint
from numpy import sign

from common import UP, DOWN
from field import FIELD_W, FIELD_H


class Bot:
    ''' Baseclass for bot '''
    def __init__(self, battle, slider, goal):
        self.battle = battle
        self.slider = slider
        self.goal = goal
        self.ball = battle.get_ball()
        self.slider_direction = 0
        self.fault_dy = 0
        self.need_move_slider_to_center = False

    def process(self):
        self.process_slider()

    def calc_slider_direction(self):
        raise NotImplementedError

    def process_slider(self):
        raise NotImplementedError

    def check_need_move_slider_to_center(self):
        if not self.need_move_slider_to_center:
            ball_x = self.ball.rect.centerx
            slider_x = self.slider.rect.centerx
            distandtion_center_ball = fabs(FIELD_W/2 - ball_x)
            distandtion_center_slider = fabs(FIELD_W/2 - slider_x)
            distandtion_ball_slider = fabs(ball_x - slider_x)
            is_ball_behind_slider = (
                distandtion_ball_slider < FIELD_W/2 and
                distandtion_center_ball >= distandtion_center_slider
            )
            if is_ball_behind_slider:
                self.need_move_slider_to_center = True


class EasyBot(Bot):
    ''' Low level bot (almost dummy) for testing '''
    def process_slider(self):
        self.check_need_move_slider_to_center()
        self.calc_slider_direction()
        if self.slider_direction:
            self.slider.process(self.slider_direction)
        elif self.need_move_slider_to_center:
            self.need_move_slider_to_center = False

    def calc_slider_direction(self):
        self.slider_direction = -sign(self.ball.dy)


class NormalBot(Bot):
    ''' Medium level bot (default) '''
    def process_slider(self):
        self.check_need_move_slider_to_center()
        self.calc_slider_direction()
        if self.slider_direction:
            self.slider.process(self.slider_direction)
        elif self.need_move_slider_to_center:
            self.need_move_slider_to_center = False

    def calc_slider_direction(self):
        slider_y = self.slider.rect.centery
        if self.need_move_slider_to_center:
            self.slider_direction = -sign(FIELD_H/2 - slider_y)
            return

        if not self.fault_dy:
            self.fault_dy = randint(-125, 125)

        ball_y = self.ball.rect.centery
        distantion_y = slider_y - ball_y + self.fault_dy
        new_directon = sign(distantion_y)
        if new_directon != self.slider_direction:
            self.slider_direction = new_directon
            self.fault_dy = 0


class HardBot(Bot):
    ''' High level bot '''
    def process_slider(self):
        self.check_need_move_slider_to_center()
        self.calc_slider_direction()
        if self.slider_direction:
            self.slider.process(self.slider_direction)
        elif self.need_move_slider_to_center:
            self.need_move_slider_to_center = False

    def calc_slider_direction(self):
        slider_centery = self.slider.rect.centery
        if self.need_move_slider_to_center:
            self.slider_direction = -sign(FIELD_H/2 - slider_centery)
            return

        abs_ball_dx = fabs(self.ball.dx)
        abs_ball_dy = fabs(self.ball.dy)
        goal_top = self.goal.top
        goal_bottom = self.goal.bottom
        if abs_ball_dx > abs_ball_dy:
            if goal_bottom <= slider_centery <= goal_top:
                self.slider_direction = 0
                return

        if abs_ball_dy > abs_ball_dx and (
           self.ball.rect.centery < 40 or
           self.ball.rect.centery > FIELD_H - 40
        ):
            if (self.slider.rect.bottom >= goal_bottom or
                self.slider.rect.top <= goal_top):
                self.slider_direction = 0
                return

        if not self.fault_dy:
            self.fault_dy = randint(-10, 10)

        ball_y = self.ball.rect.centery
        slider_top = self.slider.rect.top
        slider_bottom = self.slider.rect.bottom
        near_slider_point_to_ball = slider_top
        if fabs(ball_y-slider_bottom) < fabs(ball_y-slider_top):
            near_slider_point_to_ball= slider_bottom
        distantion_y = near_slider_point_to_ball - ball_y + self.fault_dy
        new_directon = sign(distantion_y)
        if new_directon != self.slider_direction:
            self.slider_direction = new_directon
            self.fault_dy = 0

    def check_need_move_slider_to_center(self):
        super(HardBot, self).check_need_move_slider_to_center()
        if not self.need_move_slider_to_center:
            ball_dx = self.ball.dx
            goal_rel_dist_center = FIELD_W/2 - self.goal.pos_x
            ball_moves_from_goal = sign(ball_dx) == sign(goal_rel_dist_center)
            if ball_moves_from_goal:
                self.need_move_slider_to_center = True
