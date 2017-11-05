#!/usr/bin/python

import pygame, math, random
from field_defs import *
from ball_defs  import *
from phys_defs  import *

class Ball(pygame.sprite.Sprite):
     def __init__(self, 
                  sfce,                           # deprecated (?) 
                  bkgImg,
                  start_x   = 200, 
                  start_y   = 500, 
                  color     = None,             # deprecated (?) 
                  radius    = BALL_RAD, 
                  start_ang = -40, 
                  start_vel = BALL_SPEED, 
                  max_vel   = MAX_BALL_SPEED, 
                  delta_vel = BALL_DELTA_VEL) :

          pygame.sprite.Sprite.__init__(self)
          image = pygame.image.load('pic/ball_blue.png')
          self.image = pygame.transform.scale(image, (radius, radius))
          self.sfce = sfce
          self.bkgImg = bkgImg
          self.rect  = self.image.get_rect()
          self.rad   = radius 
          self.rect.x = start_x
          self.rect.y = start_y
          self.ang = start_ang
          self.vel = start_vel
          self.max_vel   = max_vel
          self.delta_vel = delta_vel 

     def Move(self, sliders, posts):
          shift_x = self.vel*math.cos(math.radians(self.ang))
          shift_y = self.vel*math.sin(math.radians(self.ang))
          self.rect.x += shift_x
          self.rect.y += shift_y

          collision = self.ChkCollision(shift_x, shift_y, sliders, posts)
          if self.ChAngle(collision) or collision:
               if self.vel < self.max_vel: self.vel += self.delta_vel

     def ChkCollision(self, shift_x, shift_y, Sliders = None, Posts = None):
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
               y_t = slider.rect.top + slider.width/2
               y_b = slider.rect.bottom - slider.width/2 
               
               if self.rect.top + shift_y < y_b and self.rect.bottom + shift_y > y_t: 
                    # hit from right 
                    if ( self.rect.centerx > x_l and 
                         self.rect.centerx - self.rad + shift_x < x_r ):           
                         self.rect.left = x_r + self.rad
                         return HOR   

                    # hit from left 
                    if ( self.rect.centerx < x_r and 
                         self.rect.centerx + self.rad  + shift_x > x_l ):
                         self.rect.right = x_l
                         return HOR
          
          for post in Posts:
               x_c = post.rect.centerx
               y_c = post.rect.centery

               if (self.rect.centerx + shift_x - x_c)**2 + (self.rect.centery + shift_y - y_c)**2 < (self.rad + post.size/2)**2:
                    b = math.fabs(y_c - self.rect.centery)
                    c = math.sqrt((self.rect.centerx - x_c)**2 + (self.rect.centery - y_c)**2)
                    angle_collide = math.asin(b/c) if self.rect.centerx > x_c else math.pi-math.asin(b/c) # radians
                    angle_collide *= 1 if self.rect.centery > y_c else -1

                    self.rect.centerx = x_c + c * math.cos(angle_collide)
                    self.rect.centery = y_c + c * math.sin(angle_collide)
                    self.ang = math.degrees(angle_collide)
                    return 5 
          return None

     def ChAngle(self, axis):
          if   axis == HOR : self.ang = math.degrees(math.pi) - self.ang
          elif axis == VER : self.ang *= -1         
          else: return None
          self.ang = (self.ang + random.randint(-RND_ANG_DISPERS, RND_ANG_DISPERS)) % int(2*math.degrees(math.pi))
