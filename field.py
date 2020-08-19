import pygame

from common import load_image
from colors import PURPLE

from immovable_object import Line, Post, Net


FIELD_W = 800
FIELD_H = 600
BACKGROUND_COLOR = PURPLE
BORDER_HEIGHT = 20
NET_SIZE = 30
GOAL_AREA = NET_SIZE
L_GOAL_LINE = GOAL_AREA
R_GOAL_LINE = FIELD_W - GOAL_AREA
GOAL_LINE_SIZE_PERCENT = 0.6
NET_DENSE = 25
POST_SIZE = 30
POST_OFFSET_Y = int((FIELD_H-FIELD_H*GOAL_LINE_SIZE_PERCENT)/2) + POST_SIZE/2
POST_BOT_Y = FIELD_H - POST_OFFSET_Y
POST_LEFT_X = L_GOAL_LINE
POST_TOP_Y = POST_OFFSET_Y
POST_RIGHT_X = R_GOAL_LINE
GOAL_LINE_WIDTH = 22
GOAL_LINE_HEIGHT = POST_BOT_Y - POST_TOP_Y

BORDER_TOP_IMG = 'border_top'
BORDER_BOT_IMG = 'border_bot'
BORDER_SIDE_IMG = 'border_side'
CENTER_LINE_IMG = 'center_line'
GOAL_LINE_IMG = 'goal_line'


class Field:
    background_image = 'field_bg'

    def __init__(self, surface, width = FIELD_W, height = FIELD_H):
        self.background_surface = surface
        self.size = (width, height)
        self.width = width
        self.height = height
        self.rect = pygame.Rect((0, 0), self.size)
        self.surface = None
        self.posts = pygame.sprite.Group([])
        self.goals = pygame.sprite.Group([])

    def present(self):
        self.create_surface()

        self.create_nets()
        self.create_borders()
        self.create_goal_lines()
        self.create_center_line()
        self.create_posts()

        self.draw()

    def create_surface(self):
        background_sprite = load_image(self.background_image)
        self.surface = pygame.transform.scale(background_sprite, self.size)

    def draw(self):
        self.background_surface.blit(self.surface, (0, 0))

    def create_borders(self):
        Line(
            self.surface, (POST_LEFT_X, (POST_TOP_Y+POST_BOT_Y)/2),
            GOAL_LINE_IMG
        )
        Line(
            self.surface, (POST_RIGHT_X, (POST_TOP_Y+POST_BOT_Y)/2),
            GOAL_LINE_IMG
        )

        Line(
            self.surface, (0, 0),
            BORDER_TOP_IMG, size = (self.width, BORDER_HEIGHT)
        )
        Line(
            self.surface, (0, FIELD_H - BORDER_HEIGHT),
            BORDER_BOT_IMG, size = (self.width, BORDER_HEIGHT)
        )

    def create_center_line(self):
        Line(
            self.surface, (self.rect.centerx, self.rect.centery),
            CENTER_LINE_IMG
        )

    def create_goal_lines(self):
        self.left_goal_line = Line(
            self.surface, (POST_LEFT_X - GOAL_LINE_WIDTH/2, POST_TOP_Y),
            BORDER_SIDE_IMG, self.goals,
            (GOAL_LINE_WIDTH, GOAL_LINE_HEIGHT)
        )
        self.right_goal_line = Line(
            self.surface, (POST_RIGHT_X - POST_SIZE/4, POST_TOP_Y),
            BORDER_SIDE_IMG, self.goals,
            (GOAL_LINE_WIDTH, GOAL_LINE_HEIGHT)
        )

    def create_nets(self):
        Net(
            self.surface, (NET_SIZE/2, FIELD_H/2),
            size = (NET_SIZE, FIELD_H),
            crop_rect = (0, 0, NET_SIZE, FIELD_H)
        )
        Net(
            self.surface, (FIELD_W - (NET_SIZE)/2, FIELD_H/2),
            size = (NET_SIZE, FIELD_H),
            crop_rect = (0, 0, NET_SIZE, FIELD_H)
        )

    def create_posts(self):
        Post(self.surface, (POST_RIGHT_X, POST_TOP_Y), group = self.posts)
        Post(self.surface, (POST_RIGHT_X, POST_BOT_Y), group = self.posts)
        Post(self.surface, (POST_LEFT_X, POST_TOP_Y), group = self.posts)
        Post(self.surface, (POST_LEFT_X, POST_BOT_Y), group = self.posts)
