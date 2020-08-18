import math

from base_object import BaseObject
from round_object import RoundObject


SPARKLE_SIZE = 7
SPARKLE_TTL = 250
SPARKLE_SPEED = 4
SPARKLE_ACCELERATION = 0.11
SPARKLE_DANG = 0.22


class Sparkle(RoundObject):
    image_path = 'sparkle'
    dang = SPARKLE_DANG
    size = (SPARKLE_SIZE, SPARKLE_SIZE)
    ttl = SPARKLE_TTL
    start_speed = SPARKLE_SPEED
    radius = SPARKLE_SIZE/2
    acceleration = SPARKLE_ACCELERATION

    def __init__(self, *args, **kwargs):
        super(Sparkle, self).__init__(*args, **kwargs)
        self.current_ttl = self.ttl
        self.current_speed = self.start_speed
        self.start_angle = self.get_random_angle()

    def process(self, dt):
        if self.current_ttl > 0:
            self.move()
            self.current_ttl -= dt
            return True
        else:
            self.kill()
            return False

    def move(self):
        self.rect.x += self.current_speed*math.cos(self.angle)
        self.rect.y += self.current_speed*math.sin(self.angle)
        self.angle += self.dang
        self.current_speed += self.acceleration

    def reborn(self):
        self.add(self.group)
        self.current_ttl = self.ttl
        self.current_speed = self.start_speed
