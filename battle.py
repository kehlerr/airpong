from collections import namedtuple
import pygame
from pygame import USEREVENT
from pygame.locals import K_ESCAPE, KEYDOWN, KEYUP, K_UP, K_DOWN, \
         K_w, K_s, QUIT

from menu_ui import MenuPause, MenuEnd
from ball import Ball
from field import Field, L_GOAL_LINE, R_GOAL_LINE
from slider import Slider, SLIDER_DISTX
from bots import EasyBot, NormalBot, HardBot
from scoreboard import ScoreBoard
from animation import Animation
from common import UP, DOWN, DISPLAY_SIZE



PUTTING_BALL_WAIT = 500
ONSTART_PUTTING_BALL_WAIT = 2000
EV_MODIFY_BATTLE = USEREVENT + 1
EV_CLEAR_MODIFICATIONS = EV_MODIFY_BATTLE + 1
EV_PUT_BALL = USEREVENT + 3
SCOREBOARD_POS = (900, 300)


class Battle:
    goals_target = 10

    def __init__(self, display):
        self.display = display
        self.animations_mgr = Animation()
        self.surface = pygame.Surface(DISPLAY_SIZE, pygame.SRCALPHA, 32)
        self.field = Field(self.surface)
        self.scoreboard = ScoreBoard(self.surface, SCOREBOARD_POS)
        self.pause_menu = MenuPause(self.display, self)
        self.menu_pos = (
            (self.field.rect.width-self.pause_menu.width)/2,
            (self.field.rect.height-self.pause_menu.height)/2
        )
        self.menu_end = None
        self.score = (0, 0)
        self.sprites = pygame.sprite.RenderPlain()
        self.sliders = []
        self.goals = {}
        self.balls = []
        self.state = 'need_wait_put_ball'
        self.pressing_escape = False
        self.modified = False
        self.present()

    def present(self):
        self.field.present()
        self.fill_goals()
        self.create_sliders()
        self.add_ball_to_battle()
        self.bot_player = NormalBot(self, self.right_slider, self.right_goal)
        self.update_score()
        pygame.time.set_timer(EV_PUT_BALL, 1500)
        self.display.blit(self.surface, ((0,0), DISPLAY_SIZE))
        pygame.display.update(((0,0), DISPLAY_SIZE))

    def reset(self):
        self.score = (0, 0)
        self.update_score()
        self.menu_end.hide()
        self.menu_end = None
        for slider in self.sliders:
            slider.put()
        self.update_state('need_wait_put_ball')

    def update(self, main_events_loop, ticks):
        for sprite in self.sprites:
            sprite.clear(self.surface)

        main_events_loop(self)
        self.animations_mgr.update(ticks)

        if self.check_state('play'):
            self.on_play_state()
        elif self.check_state('need_wait_put_ball'):
            self.on_need_wait_put_ball()
        if self.check_state('pause'):
            self.on_pause_state()
            return
        elif self.check_state('end'):
            return

        for sprite in self.sprites:
            sprite.draw(self.surface)
        self.display.blit(self.surface, (0,0))
        pygame.display.update(self.field.rect)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            self.on_key_down()
        elif event.type == KEYUP:
            self.on_key_up()
        elif event.type == USEREVENT:
            self.handle_user_event(event)
        elif event.type == EV_MODIFY_BATTLE:
            self.modify()
        elif event.type == EV_CLEAR_MODIFICATIONS:
            self.clear_modifications()
        elif event.type == EV_PUT_BALL:
            self.update_state('play')
            pygame.time.set_timer(EV_PUT_BALL, 0)

    def on_key_down(self):
        is_pressed = pygame.key.get_pressed()

        if not self.check_state('pause'):
            if is_pressed[K_ESCAPE]:
                self.pressing_escape = True
                self.pause_game()
                return

        if is_pressed[K_w]:
            self.left_slider.process(UP)
        if is_pressed[K_s]:
            self.left_slider.process(DOWN)
        if is_pressed[K_UP]:
            self.right_slider.process(UP)
        if is_pressed[K_DOWN]:
            self.right_slider.process(DOWN)

    def on_key_up(self):
        is_pressed = pygame.key.get_pressed()
        if not (is_pressed[K_w] and is_pressed[K_s]):
            self.left_slider.on_change_direction()
        if not (is_pressed[K_UP] and is_pressed[K_DOWN]):
            self.right_slider.on_change_direction()

        self.pressing_escape = False

    def handle_user_event(self, event):
        event_info = event.__dict__
        for key in event_info:
            if key == 'goal':
                self.on_goal_scored(event_info)

            if key == 'pause':
                self.update_state('need_wait_put_ball')

    def update_score(self, d_score=(0,0)):
        self.score = (self.score[0] + d_score[0], self.score[1] + d_score[1])
        self.scoreboard.set_score(self.score)
        self.display.blit(self.surface, (0, 0))
        pygame.display.update(self.scoreboard.rect)

    def update_state(self, state):
        self.state = state

    def check_state(self, state):
        return self.state == state

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
        collision_objects = {
            'sliders': self.sliders,
            'goals': self.field.goals.sprites(),
            'posts': self.field.posts.sprites(),
            'balls': self.balls
        }
        ball = Ball(self.field.surface, self.field.rect.center,
                    self.sprites, collision_objects, self.animations_mgr)
        self.balls.append(ball)

    def fill_goals(self):
        Goal = namedtuple('Goal', ['pos_x', 'top', 'bottom'])
        left_goal = self.field.left_goal_line
        self.left_goal = Goal(
            left_goal.rect.centerx,
            left_goal.rect.top,
            left_goal.rect.bottom
        )

        right_goal = self.field.right_goal_line
        self.right_goal = Goal(
            right_goal.rect.centerx,
            right_goal.rect.top,
            right_goal.rect.bottom
        )

    def get_ball(self):
        return self.balls[0]

    def create_sliders(self):
        left_pos = (L_GOAL_LINE + SLIDER_DISTX, self.field.rect.centery)
        self.left_slider = Slider(
            self.field.surface, left_pos, group = self.sprites,
            color = 'red'
        )
        self.sliders.append(self.left_slider)

        right_pos = (R_GOAL_LINE - SLIDER_DISTX, self.field.rect.centery)
        self.right_slider = Slider(
            self.field.surface, right_pos, group = self.sprites,
            color = 'blue'
        )
        self.sliders.append(self.right_slider)

    def on_play_state(self):
        self.process_objects()
        self.bot_player.process()

    def on_pause_state(self):
        active_menu = self.menu_end or self.pause_menu
        active_menu.update()

    def process_objects(self):
        for ball in self.balls:
            ball.update()

    def on_goal_scored(self, scored_info):
        if scored_info['goal'] == 1:
            self.update_score((1, 0))
        else:
            self.update_score((0, 1))
        self.clear_modifications()
        if max(self.score) == self.goals_target:
            self.end_game()
        else:
            self.update_state('need_wait_put_ball')

    def on_need_wait_put_ball(self):
        self.update_state('waiting_put_ball')
        pygame.time.set_timer(EV_PUT_BALL, 500)

    def pause_game(self):
        self.update_state('pause')
        self.pause_menu.set_position(self.menu_pos)
        self.pause_menu.show()
        continue_btn = self.pause_menu.get_widget('continue_btn')
        continue_btn.set_onpressed(self.continue_game)
        quit_btn = self.pause_menu.get_widget('quit_btn')
        quit_btn.set_onpressed(self.quit_game)

    def continue_game(self):
        self.update_state('play')
        self.pause_menu.hide()

    def end_game(self):
        self.update_state('pause')
        menu = MenuEnd(self.display, self)
        menu.set_position(self.menu_pos)
        menu.load_layout()
        win_icon = menu.get_widget('win_icon')
        lose_icon = menu.get_widget('lose_icon')
        if self.score[0] > self.score[1]:
            win_icon.visible = True
            lose_icon.visible = False
        else:
            win_icon.visible = False
            lose_icon.visible = True
        menu.show()
        self.menu_end = menu
        continue_btn = menu.get_widget('continue_btn')
        continue_btn.set_onpressed(self.reset)
        quit_btn = menu.get_widget('quit_btn')
        quit_btn.set_onpressed(self.quit_game)


    def quit_game(self):
        pygame.event.clear()
        ev = pygame.event.Event(QUIT)
        pygame.event.post(ev)
