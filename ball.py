#!/usr/bin/python

import pygame, math
from field_defs import *
from ball_defs  import *
from color_defs import *
from phys_defs  import *

class Ball(pygame.sprite.Sprite):
     def __init__(self, sfce, start_x = FIELD_W/2, start_y = FIELD_H/2, color = BALL_CL, rad = BALL_RAD, start_angle = -45, start_vel=BALL_SPEED, max_vel=MAX_BALL_SPEED, delta_vel=BALL_DELTA_VEL):
          pygame.sprite.Sprite.__init__(self)
          self.sfce = sfce
          self.center_point = (start_x, start_y)
          self.rad = rad 
          self.angle = start_angle
          image = pygame.image.load('pic/ball_spr1.png')
          self.image = pygame.transform.scale(image, (self.rad, self.rad))
          self.rect = self.image.get_rect()
          self.rect.x = start_x
          self.rect.y = start_y
          self.vel = start_vel
          self.max_vel = max_vel
          self.delta_vel = delta_vel 

     def Move(self, sliders):
          self.rect.x += self.vel*math.cos(math.radians(self.angle))
          self.rect.y += self.vel*math.sin(math.radians(self.angle))
          collide = self.ChkCollision(sliders)
          if collide is not None:
               self.ChAngle(collide)
               if self.vel < self.max_vel: self.vel += self.delta_vel
     
     def ChAngle(self, axis):
          if axis == HOR : self.angle = math.degrees(math.pi) - self.angle
          elif axis == VER : self.angle *= -1         

     def ChkCollision(self, Sliders = None):
          if self.rect.y < 0: 
               self.rect.y = 0 
               return VER

          if self.rect.y + self.rad > FIELD_H: 
               self.rect.y = FIELD_H - self.rad
               return VER
                
          if self.rect.left < L_GOAL_LINE:
               self.rect.left = L_GOAL_LINE + self.rad
               return HOR
               
          if self.rect.right > R_GOAL_LINE:
               self.rect.right = R_GOAL_LINE - 1
               return HOR
          
          for slider in Sliders:
               x_l = slider.rect.left + self.rad
               x_r = slider.rect.right - self.rad
               x_c = slider.rect.centerx
               y_t = slider.rect.top - self.rad
               y_b = slider.rect.bottom + self.rad

               if self.rect.x < x_c and self.rect.x + self.rad > x_l and (self.rect.y < y_b and self.rect.y > y_t):
                    self.rect.x = x_l - self.rad
                    return HOR

               if self.rect.x > x_c and self.rect.x - self.rad < x_r and (self.rect.y < y_b and self.rect.y > y_t):
                    self.rect.x = x_r + self.rad
                    return HOR   
                           
          return None
