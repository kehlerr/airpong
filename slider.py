import pygame

from base_object import BaseObject
from field  import GOAL_AREA, FIELD_H


SLIDER_DISTX = GOAL_AREA * 3
SLIDER_H = 150
SLIDER_W = 30


class Slider(BaseObject):
    size = (SLIDER_W, SLIDER_H)
    max_speed = 15
    acceleration = 0.75

    def __init__(self, *args, group = None, color = None):
        self.image_path = f'pic/slider_{color}.png'
        super(Slider, self).__init__(*args, group = group)
        self.speed = 1
        self.direction = 1

    def move(self, direction):
        if direction != self.direction:
            self.direction = direction
            self.on_change_move()
        else:
            self.speed += self.acceleration
            self.speed = min(self.speed, self.max_speed)
        self.rect.centery -= self.direction * self.speed
        self.check_borders()

    def on_change_move(self):
        if self.speed > 1:
            self.speed = 1

    def check_borders(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > FIELD_H:
            self.rect.bottom = FIELD_H

    def get_primitive_view(self):
        surface = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        radius = int(SLIDER_W/2)
        rect = (0, radius, SLIDER_W, SLIDER_H- radius*2)
        pygame.draw.rect(surface, self.primitive_color, rect)
        pygame.draw.circle(
            surface, self.primitive_color,
            (radius, radius), radius
        )
        pygame.draw.circle(
            surface, self.primitive_color,
            (radius, SLIDER_H - radius), radius
        )
        return surface
