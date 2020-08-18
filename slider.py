import random
from pygame import Surface, draw, SRCALPHA

from base_object import BaseObject
from field import GOAL_AREA, FIELD_H
from common import UP, DOWN


SLIDER_DISTX = GOAL_AREA * 3
SLIDER_H = 150
SLIDER_W = 30


class Slider(BaseObject):
    size = (SLIDER_W, SLIDER_H)
    max_speed = 15
    acceleration = 0.75

    def __init__(self, *args, group = None, color = None):
        self.image_path = f'slider_{color}'
        super(Slider, self).__init__(*args, group = group)
        self.speed = 1
        self.direction = random.choice([UP, DOWN])

    def process(self, direction):
        if direction != self.direction:
            self.change_direction(direction)
        if self.can_move():
            self.move()
            return True
        else:
            limit_y = self.direction*(FIELD_H/2 - self.height/2-1)
            self.rect.centery = FIELD_H/2 - limit_y
            return False

    def can_move(self):
        if self.direction == UP:
            return self.rect.top > 1
        elif self.direction == DOWN:
            return self.rect.bottom < FIELD_H-1

    def move(self):
        self.speed += self.acceleration
        self.speed = min(self.speed, self.max_speed)
        self.rect.centery -= self.direction * self.speed

    def change_direction(self, direction):
        self.direction = direction
        self.on_change_direction()

    def on_change_direction(self):
        if self.speed > 1:
            self.speed = 1

    def get_primitive_view(self):
        surface = Surface(self.size, SRCALPHA, 32)
        radius = int(SLIDER_W/2)
        rect = (0, radius, SLIDER_W, SLIDER_H- radius*2)
        draw.rect(surface, self.primitive_color, rect)
        draw.circle(
            surface, self.primitive_color,
            (radius, radius), radius
        )
        draw.circle(
            surface, self.primitive_color,
            (radius, SLIDER_H - radius), radius
        )
        return surface
