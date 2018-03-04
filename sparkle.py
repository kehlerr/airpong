import math

import obj_template

SPARKLE_SIZE = 7
SPARKLE_TTL = 30
SPARKLE_VEL = 5
SPARKLE_ANG = 45
SPARKLE_DANG = 15
SPARKLE_IMG = 'pic/sparkle.png'


class Sparkle(obj_template.T):
    def __init__(self,
                 spr_img,
                 pos,
                 size=SPARKLE_SIZE,
                 ang=SPARKLE_ANG,
                 dang=SPARKLE_DANG,
                 ttl=SPARKLE_TTL,
                 vel=SPARKLE_VEL,
                 group=None
                ):
        obj_template.T.__init__(self, spr_img, (size, ), pos, group)
        self.ttl = ttl
        self.vel = vel
        self.ang = ang
        self.dang = dang

    def live(self):
        if self.ttl > 0:
            self.move()
            self.ttl -= 1
            self.vel -= 0.4
        else:
            self.__del__()

    def move(self):
        self.rect.x -= self.vel*math.cos(math.radians(self.ang))
        self.rect.y += self.vel*math.sin(math.radians(self.ang))
        self.ang += self.dang
