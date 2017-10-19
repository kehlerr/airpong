#!/usr/bin/python

import pygame
from slider_defs import *
from field_defs  import *
from color_defs  import *

global SLIDERS 
SLIDERS = []

class SliderBate(pygame.sprite.Sprite):
    
     def __init__(self, sfce, pos_x, pos_y, height = SLIDER_H, width = SLIDER_W):
          pygame.sprite.Sprite.__init__(self)
          SLIDERS.append(self)
          self.sfce = sfce
          image = pygame.image.load('pic/slider2.png')
          self.image = pygame.transform.scale(image, (width, height))
          self.rect = self.image.get_rect() 
          self.rect.x = pos_x
          self.rect.y = pos_y
         
     def Move(self, direct, velocity=1):
          delta = direct * velocity
          self.rect.centery -= delta
              
          if self.rect.top < 0 : self.rect.top = 0 
          if self.rect.bottom > FIELD_H : self.rect.bottom = FIELD_H
