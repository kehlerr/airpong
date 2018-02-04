import pygame
from common import X, Y


class T(pygame.sprite.Sprite):
    def __init__(self, spr_img, size, pos, group=None, sfce=None):
        pygame.sprite.Sprite.__init__(self)

        if group is not None:
            group.add(self)

        self.sfce = sfce
        self.size = min(size)
#       TODO: handle exception here if img not found
        self.image = pygame.image.load(spr_img)
        if size[X] is not 0:
            width = size[X]
            height = size[Y] if len(size) > 1 else size[X]
            self.image = pygame.transform.scale(self.image, (width, height))

#       self.image.set_colorkey(BLACK)
#       self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.moveto(pos)
        if sfce is not None:
            self.sfce = sfce
            self.sfce.blit(self.image, self.rect)

    def move(self, dx=0, dy=0):
        self.rect.move(dx,dy)

    def moveto(self, pos):
        self.rect.center = pos