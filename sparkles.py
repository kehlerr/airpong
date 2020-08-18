from math import pi

from sparkle import Sparkle


class Sparkles:
    max_sparkles_amount = 150

    def __init__(
            self, background_surface, animations_mgr,
            image_path = None, group = None
        ):
        self.background_surface = background_surface
        self.animations_mgr = animations_mgr
        self.image_path = image_path
        self.group = group
        self.items = []
        self.fill_sparkles_items()

    def fill_sparkles_items(self):
        for _ in range(self.max_sparkles_amount):
            sparkle = Sparkle(
                self.background_surface, (0, 0),
                image_path = self.image_path, group = self.group
            )
            self.items.append(sparkle)

    def generate_sparkles(self, amount, center_pos):
        for i in range(amount):
            if not self.items[i].alive():
                self.items[i].reborn()
            self.items[i].put(
                pos = center_pos, angle = Sparkle.get_random_angle()
            )
            self.animations_mgr.add(self.items[i])
