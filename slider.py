#!/usr/bin/python

import obj_template
from slider_defs import *
from field_defs  import *

class Slider(obj_template.T):

    def Move(self, direct, velocity=1):
        delta = direct * velocity
        self.rect.centery -= delta
        if self.rect.top < 0 : self.rect.top = 0
        if self.rect.bottom > FIELD_H : self.rect.bottom = FIELD_H
