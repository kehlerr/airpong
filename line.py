import pygame

from immovable_object import ImmovableObject
from common import X, Y


class Line(ImmovableObject):
    size = None

    def __init__(
        self, background_surface, pos, image_path, group = None, size = None
    ):
        center_pos = pos
        if size:
            center_pos = (pos[X] + size[X]/2, pos[Y] + size[Y]/2)
        super(Line, self).__init__(
            background_surface, center_pos, image_path, group, size
        )

    def get_primitive_view(self):
        if not self.size:
            self.size = (1, 1)
        surface = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        pos = (
            self.start_pos[X] - self.size[X] / 2,
            self.start_pos[Y] - self.size[Y] / 2
        )
        rect = pygame.Rect(pos, self.size)
        pygame.draw.rect(surface, self.primitive_color, rect)
        return surface
