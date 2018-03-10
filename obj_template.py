# --*- coding: utf-8 -*-

import pygame

from common import X, Y
#from color_defs import WHITE

# TODO [low]: добавить кроп имги


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

#        self.image.set_colorkey(WHITE)
#       self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.start_pos = pos
        self.put(pos=pos)
        if sfce is not None:
            self.sfce = sfce
            self.sfce.blit(self.image, self.rect)

    def __del__(self):
        self.kill()

    def draw(self):
        self.sfce.blit(self.image, self.rect)

    def move(self, dx=0, dy=0):
        self.rect.move(dx,dy)

    def moveto(self, pos):
        self.rect.center = pos

    def put(self, pos=None, rect=None):
        self.moveto(pos if pos else self.start_pos)
        if rect:
            self.rect = rect
