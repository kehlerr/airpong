#!/usr/bin/python

import pygame, math
from field_defs import *
from ball_defs  import *
from phys_defs  import *

class Ball(pygame.sprite.Sprite):
     def __init__(self, 
                  sfce,                           # deprecated (?) 
                  bkgImg,
                  start_x   = 400, 
                  start_y   = 50, 
                  color     = None,             # deprecated (?) 
                  radius    = BALL_RAD, 
                  start_ang = -180, 
                  start_vel = BALL_SPEED, 
                  max_vel   = MAX_BALL_SPEED, 
                  delta_vel = BALL_DELTA_VEL) :

          pygame.sprite.Sprite.__init__(self)
          image = pygame.image.load('pic/ball_spr1.png')
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
          dx = 1 if shift_x > 0 else -1
          dy = 1 if shift_y > 0 else -1
          for movs in range(int(max(math.fabs(shift_x), math.fabs(shift_y)))):
                    dx = dx if math.fabs(shift_x) > movs else 0
                    dy = dy if math.fabs(shift_y) > movs else 0
                    self.sfce.blit(self.bkgImg, self.rect, self.rect)
                    self.rect.x += dx 
                    self.rect.y += dy
                    self.sfce.blit(self.image, self.rect)       

          self.sfce.blit(self.bkgImg, self.rect, self.rect)
          collision = self.ChkCollision(shift_x, shift_y, sliders, posts)
          self.sfce.blit(self.image, self.rect)       

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
#                    if (self.rect.left + shift_x - x_r)**2  < (self.rad)**2:
                         self.rect.left = x_r
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
