import pygame

from common import X, Y
import color_defs as colors


class BaseObject(pygame.sprite.Sprite):
    primitive_color = colors.SNOW

    def __init__(
            self,
            background_surface,
            start_pos,
            image_path = None,
            group = None,
            size = None,
            angle = None,
            crop_rect = None
        ):
        super(BaseObject, self).__init__()

        self.background_surface = background_surface
        self.start_pos = start_pos
        if size:
            self.size = size
        self.default_size = None
        self.start_angle = angle

        if image_path:
            self.image_path = image_path
        self.create_view()

        self.rect = None
        self.width = None
        self.height = None
        self.radius = None
        self.setup_size()
        self.update_view_size()

        self.surface = None
        self.create_surface()

        self.put()

        if group is not None:
            self.group = group
            group.add(self)

        self.crop_rect = crop_rect

    def create_view(self):
        try:
            if self.image_path:
                self.image = pygame.image.load(self.image_path)
                self.default_size = self.image.get_size()
            else:
                self.image = self.get_primitive_view()
        except pygame.error:
            self.image = self.get_primitive_view()

    def get_primitive_view(self):
        raise NotImplementedError

    def create_surface(self):
        surface = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        surface.blit(self.image, self.rect)
        self.surface = surface.convert_alpha()

    def setup_size(self):
        if self.size:
            width = int(self.size[X])
            height = int(self.size[Y])
            self.size = (width, height)
        else:
            self.size = self.default_size

    def update_view_size(self):
        self.radius = min(self.size)/2
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    def draw(self, on_surface = None):
        background = on_surface or self.background_surface
        background.blit(self.surface, self.rect, self.crop_rect)

    def clear(self, from_surface, rect = None):
        if not rect:
            rect = self.rect
        from_surface.blit(self.background_surface, rect, rect)

    def put(self, pos = None, rect = None, angle = None):
        if pos:
            self.moveto(pos)
        else:
            self.moveto(self.start_pos)

        if rect:
            self.rect = rect

        if angle:
            self.angle = angle
        else:
            self.angle = self.start_angle

    def move(self, dx = 0, dy = 0):
        self.rect.move_ip(dx, dy)

    def moveto(self, pos):
        self.rect.center = pos

    def __del__(self):
        self.kill()
