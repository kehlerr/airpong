from math import pi

from sparkle import Sparkle

MIN_SPARKLES_AMOUNT = 75
MAX_SPARKLES_AMOUNT = 150

class Sparkles:
    def __init__(
            self, background_surface, thread, image_path = None, group = None
        ):
        self.background_surface = background_surface
        self.thread = thread
        self.image_path = image_path
        self.group = group
        self.items = []
        self.fill_sparkles_items()

    def fill_sparkles_items(self):
        self.items = [
            Sparkle(
                self.background_surface, (0, 0),
                image_path = self.image_path, group = self.group
            )
            for _ in range(MAX_SPARKLES_AMOUNT)
        ]

    def generate_sparkles(self, amount, center_pos):
        for i in range(amount):
            if not self.items[i].alive():
                self.items[i].reborn()
            self.items[i].put(
                pos = center_pos, angle = Sparkle.get_random_angle()
            )
            self.thread.add(self.items[i])
