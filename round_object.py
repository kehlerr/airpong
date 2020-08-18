from pygame import Surface, draw, SRCALPHA
from math import trunc, pi
from random import uniform

from common import X, Y
from base_object import BaseObject


class RoundObject(BaseObject):
    def get_primitive_view(self):
        truncated_radius = trunc(self.radius)
        surface = Surface(self.size, SRCALPHA, 32)
        draw.circle(
            surface, self.primitive_color,
            (truncated_radius,truncated_radius), truncated_radius
        )
        return surface

    @staticmethod
    def get_random_angle():
        return uniform(-2*pi, 2*pi)

