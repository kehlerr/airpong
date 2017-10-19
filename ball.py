#!/usr/bin/python

import pygame, math
from field_defs import *
from ball_defs  import *
from color_defs import *
from phys_defs  import *

class Ball(pygame.sprite.Sprite):
     def __init__(self, 
                  sfce,                           # deprecated (?) 
                  start_x   = FIELD_W/2, 
                  start_y   = FIELD_H/2, 
                  color     = BALL_CL,            # deprecated (?) 
                  radius    = BALL_RAD, 
                  start_ang = -190, 
                  start_vel = BALL_SPEED, 
                  max_vel   = MAX_BALL_SPEED, 
                  delta_vel = BALL_DELTA_VEL) :

          pygame.sprite.Sprite.__init__(self)
          image = pygame.image.load('pic/ball_spr1.png')
          self.image = pygame.transform.scale(image, (radius, radius))
          self.rect  = self.image.get_rect()
          self.rad   = radius 
          self.rect.x = start_x
          self.rect.y = start_y
          self.ang = start_ang
          self.vel = start_vel
          self.max_vel   = max_vel
          self.delta_vel = delta_vel 

     def Move(self, sliders):
          shift_x = self.vel*math.cos(math.radians(self.ang))
          shift_y = self.vel*math.sin(math.radians(self.ang))
          shift   = shift_x, shift_y
          collision = self.ChkCollision((shift_x, shift_y), sliders)
          if collision is not None:
               self.ChAngle(collision)
               if self.vel < self.max_vel: self.vel += self.delta_vel
          else: 
               self.rect.move_ip(shift)
          

     def ChkCollision(self, shift, Sliders = None):
          shift_x, shift_y = shift

          if   self.rect.top + shift_y < 0: 
               self.rect.y = 0 
               return VER

          if   self.rect.bottom + shift_y > FIELD_H: 
               self.rect.bottom = FIELD_H
               return VER
                
          if   self.rect.left + shift_x < L_GOAL_LINE:
               self.rect.left = L_GOAL_LINE
               return HOR
               
          if   self.rect.right + shift_x > R_GOAL_LINE:
               self.rect.right = R_GOAL_LINE
               return HOR
          
          for slider in Sliders:
               x_l = slider.rect.left
               x_r = slider.rect.right
               x_c = slider.rect.centerx
               y_t = slider.rect.top
               y_b = slider.rect.bottom 
               
               if self.rect.top + shift_y < y_b and self.rect.bottom + shift_y > y_t: 
                    # hit from right 
                    if ( self.rect.left > x_l and 
                         self.rect.right + shift_x < x_r ): 
                         self.rect.left = x_r
                         return HOR   

                    # hit from left 
                    if ( self.rect.right < x_r and 
                         self.rect.left  + shift_x > x_l ):
                         self.rect.right = x_l
                         return HOR

          return None

     def ChAngle(self, axis):
          if   axis == HOR : self.ang = math.degrees(math.pi) - self.ang
          elif axis == VER : self.ang *= -1         
