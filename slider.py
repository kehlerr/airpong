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
#          self.Draw(self.SliderRect, SNOW) 
                    
#     def Draw(self, Rect, color):
#          pygame.draw.rect(self.sfce, color, self.rect)
#          pygame.draw.circle(self.sfce, color, (self.rect.centerx, self.rect.top), SLIDER_W/2, SLIDER_W/2)
#          pygame.draw.circle(self.sfce, color, (self.rect.centerx, self.rect.bottom), SLIDER_W/2, SLIDER_W/2)
          
     def Move(self, direct, velocity=1):
#          self.Draw(self.rect, BKG_CL)

          delta = direct * velocity
          self.rect.centery -= delta

#          if self.rect.top - SLIDER_W/2 < 0 : self.rect.top = SLIDER_W/2
#          if self.rect.bottom + SLIDER_W/2 > FIELD_H : self.rect.bottom = FIELD_H - SLIDER_W/2
               
          if self.rect.top < 0 : self.rect.top = 0
          if self.rect.bottom > FIELD_H : self.rect.bottom = FIELD_H
#          self.Draw(self.SliderRect, SNOW)
           

#class Ball(pygame.sprite.Sprite):
#     def __init__(self, sfce, start_x = FIELD_W/2, start_y = FIELD_H/2, color = BALL_CL, rad = BALL_RAD, start_angle = -45, start_vel=BALL_SPEED, max_vel=MAX_BALL_SPEED, delta_vel=BALL_DELTA_VEL):
#          pygame.sprite.Sprite.__init__(self)
#          self.sfce = sfce
#          self.center_point = (start_x, start_y)
#          self.rad = rad 
#          self.angle = start_angle
#          image = pygame.image.load('pic/ball_spr1.png')
#          self.image = pygame.transform.scale(image, (self.rad, self.rad))
#          self.rect = self.image.get_rect()
#          self.rect.x = start_x
#          self.rect.y = start_y
#          self.vel = start_vel
#          self.max_vel = max_vel
#          self.delta_vel = delta_vel 

#     def Draw(self, color):
#          pygame.draw.circle(self.sfce, color, (int(self.ball_x), int(self.ball_y)), self.rad, self.rad)

