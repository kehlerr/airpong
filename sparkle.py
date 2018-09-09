import math

import obj_template

SPARKLE_SIZE = 7
SPARKLE_TTL = 300
SPARKLE_VEL = 5
SPARKLE_ANG = 45
SPARKLE_DANG = 10
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
        self.current_ttl = self.ttl
        self.vel = vel
        self.current_vel = vel
        self.ang = ang
        self.dang = dang

    def process(self, dt):
        if self.current_ttl > 0:
            self.move()
            self.current_ttl -= dt
            self.current_vel -= 0.5
            return True
        else:
            self.kill()
            return False

    def move(self):
        self.rect.x += self.vel*math.cos(math.radians(self.ang))
        self.rect.y += self.vel*math.sin(math.radians(self.ang))
        self.ang += self.dang

    def put(self, pos, ang=None, rect=None):
        obj_template.T.put(self, pos, rect)
        self.ang = ang

    def reborn(self, group):
        self.add(group)
        self.current_ttl = self.ttl
        self.current_vel = self.vel
