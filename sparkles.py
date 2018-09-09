from random import randint

from ball_defs import *
from sparkle import *


class Sparkles:
    def __init__(self, image, group, thread):
        self.group = group
        self.thread = thread
        self.items = [Sparkle(image, (0, 0)) for i in range(MAX_SPARKLES_AMOUNT)]

    def generate_sparkles(self, amount, center_pos):
        for i in range(amount):
            if not self.items[i].alive():
                self.items[i].reborn(self.group)
            self.items[i].put(center_pos, randint(-180, 180))
            self.thread.add(self.items[i])

