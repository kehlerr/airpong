#!/usr/bin/python

import pygame
import os
from field_defs import *
from color_defs import *
from post import *
from net  import *

class Field:
     
     def __init__(self, sfce, width = FIELD_W, height = FIELD_H):
          self.sfce = sfce
          self.FieldSfce = pygame.Surface((width, height))
          self.FieldRect = pygame.Rect(0, 0, width, height)
          self.bkgImg = pygame.image.load('pic/bkg7.jpeg')
          self.bkgImg = pygame.transform.scale(self.bkgImg, (width, height))
          self.Draw()
          self.bkgImg.blit(self.FieldSfce, (0,0))
          self.sfce.blit(self.bkgImg, (0,0))


     def Draw(self):          
          self.FieldSfce.blit(self.bkgImg, (0, 0))
          pygame.draw.line(self.FieldSfce, BLACK, (self.FieldRect.topleft), (self.FieldRect.bottomleft), 1)       
          pygame.draw.line(self.FieldSfce, BLACK, (self.FieldRect.topright), (self.FieldRect.bottomright), 5)
          pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.topright), (self.FieldRect.bottomright), 1)
          pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.midtop), (self.FieldRect.midbottom), 3)      
          pygame.draw.circle(self.FieldSfce, SNOW, (self.FieldRect.centerx+1, self.FieldRect.centery+1), FIELD_CENTER_SIZE, 3)
          pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.left+NET_SIZE, self.FieldRect.top), (self.FieldRect.left+NET_SIZE, self.FieldRect.bottom), 5) 
          pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.right-NET_SIZE, self.FieldRect.top), (self.FieldRect.right-NET_SIZE,self.FieldRect.bottom), 5) 

          Net(self.FieldSfce, 0, 0, NET_SIZE, FIELD_H)
          Net(self.FieldSfce, FIELD_W - NET_SIZE+1, 0, NET_SIZE, FIELD_H)
          Post(self.FieldSfce, self.FieldRect.right - NET_SIZE, self.FieldRect.top + POST_SIZE/2)
          Post(self.FieldSfce, self.FieldRect.left  + NET_SIZE, self.FieldRect.top + POST_SIZE/2)
          Post(self.FieldSfce, self.FieldRect.left  + NET_SIZE, self.FieldRect.bottom - POST_SIZE/2)
          Post(self.FieldSfce, self.FieldRect.right - NET_SIZE, self.FieldRect.bottom - POST_SIZE/2)
#          Post(self.FieldSfce, self.FieldRect.centerx+22, 310)
#          Post(self.FieldSfce, self.FieldRect.centerx, 450)
          

