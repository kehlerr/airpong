#!/usr/bin/python

import pygame
from field_defs import *
from color_defs import *
from post import *

class Field:
     
     def __init__(self, sfce, width = FIELD_W, height = FIELD_H):
          self.sfce = sfce
          self.FieldRect = pygame.Rect(0, 0, width, height)
          self.bkgImg = pygame.image.load('pic/bkg7.jpeg')
          self.bkgImg = pygame.transform.scale(self.bkgImg, (width, height))
          self.Draw()

     def Draw(self):          
          self.sfce.blit(self.bkgImg, (0, 0))
          pygame.draw.line(self.sfce, BLACK, (self.FieldRect.topleft), (self.FieldRect.bottomleft), 1)       
          pygame.draw.line(self.sfce, BLACK, (self.FieldRect.topright), (self.FieldRect.bottomright), 5)
          pygame.draw.line(self.sfce, SNOW, (self.FieldRect.topright), (self.FieldRect.bottomright), 1)
          pygame.draw.line(self.sfce, SNOW, (self.FieldRect.midtop), (self.FieldRect.midbottom), 3)      
          pygame.draw.circle(self.sfce, SNOW, (self.FieldRect.centerx+1, self.FieldRect.centery+1), FIELD_CENTER_SIZE, 3)
          pygame.draw.line(self.sfce, SNOW, (self.FieldRect.left+NET_SIZE, self.FieldRect.top), (self.FieldRect.left+NET_SIZE, self.FieldRect.bottom), 5) 
          pygame.draw.line(self.sfce, SNOW, (self.FieldRect.right-NET_SIZE, self.FieldRect.top), (self.FieldRect.right-NET_SIZE,self.FieldRect.bottom), 5) 

          Post(self.sfce, self.FieldRect.right - NET_SIZE, self.FieldRect.top + POST_SIZE/2)
          Post(self.sfce, self.FieldRect.left  + NET_SIZE, self.FieldRect.top + POST_SIZE/2)
          Post(self.sfce, self.FieldRect.left  + NET_SIZE, self.FieldRect.bottom - POST_SIZE/2)
          Post(self.sfce, self.FieldRect.right - NET_SIZE, self.FieldRect.bottom - POST_SIZE/2)
          Post(self.sfce, self.FieldRect.centerx+23, self.FieldRect.centery-52)

          for y in range(FIELD_H / NET_DENSE):
               pygame.draw.aaline(self.sfce, SNOW, (self.FieldRect.left, y*NET_DENSE), (self.FieldRect.left+NET_SIZE, (y+1)*NET_DENSE), 1) 
               pygame.draw.aaline(self.sfce, SNOW, (self.FieldRect.left+NET_SIZE, y*NET_DENSE), (self.FieldRect.left, (y+1)*NET_DENSE), 1) 
               pygame.draw.aaline(self.sfce, SNOW, (self.FieldRect.right, y*NET_DENSE), (self.FieldRect.right-NET_SIZE, (y+1)*NET_DENSE), 1) 
               pygame.draw.aaline(self.sfce, SNOW, (self.FieldRect.right-NET_SIZE, y*NET_DENSE), (self.FieldRect.right, (y+1)*NET_DENSE), 1) 
