#!/usr/bin/python

import pygame
from slider_defs import *
from field_defs  import *
from color_defs  import *
from post import *

global SLIDERS 
SLIDERS = []

class Slider(pygame.sprite.Sprite):
    
     def __init__(self, sfce, pos_x, pos_y, imgname, height = SLIDER_H, width = SLIDER_W):
          pygame.sprite.Sprite.__init__(self)
          SLIDERS.append(self)
          self.sfce = sfce
          image = pygame.image.load(imgname)
          self.image = pygame.transform.scale(image, (width, height))
        #  self.image = pygame.transform.rotate(self.image, 32)
          self.image.set_colorkey(WHITE)
          self.mask = pygame.mask.from_surface(self.image)
          self.rect = self.image.get_rect() 
          self.rect.x = pos_x - width/2
          self.rect.y = pos_y
          self.width = width
          self.height = height

     def Move(self, direct, velocity=1):
          delta = direct * velocity
          self.rect.centery -= delta
          if self.rect.top < 0 : self.rect.top = 0
          if self.rect.bottom > FIELD_H : self.rect.bottom = FIELD_H
