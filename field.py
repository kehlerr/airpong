#!/usr/bin/python

from color_defs import *
from post import *
from net  import *

BORDER_HEIGHT = 20 

global POSTS
POSTS = pygame.sprite.Group([])

class Field:
     
     def __init__(self, sfce, width = FIELD_W, height = FIELD_H):
          self.sfce = sfce
          self.FieldSfce = pygame.Surface((width, height))
          self.FieldRect = pygame.Rect(0, 0, width, height)
          self.bkgImg = pygame.image.load('pic/bkg11.jpg')
          self.bkgImg = pygame.transform.scale(self.bkgImg, (width, height))
          self.border_topImg = pygame.image.load('pic/border_top.png')
          self.border_topImg = pygame.transform.scale(self.border_topImg, (width, BORDER_HEIGHT))
          self.border_botImg = pygame.image.load('pic/border_bot.png')
          self.border_botImg = pygame.transform.scale(self.border_botImg, (width, BORDER_HEIGHT))
          self.height = height
          self.width  = width
          self.Draw()
          self.bkgImg.blit(self.FieldSfce, (0,0))
          self.sfce.blit(self.bkgImg, (0,0))


     def Draw(self):          
          self.FieldSfce.blit(self.bkgImg, (0, 0))
          center_line = pygame.image.load('pic/center_line.png')
          self.FieldSfce.blit(self.border_topImg, (0,0))
          self.FieldSfce.blit(self.border_botImg, (0, self.height - BORDER_HEIGHT))
          self.FieldSfce.blit(center_line, (self.FieldRect.centerx-45, 0))
          pygame.draw.line(self.FieldSfce, BLACK, (self.FieldRect.topleft), (self.FieldRect.bottomleft), 1)       
          pygame.draw.line(self.FieldSfce, BLACK, (self.FieldRect.topright), (self.FieldRect.bottomright), 5)
          pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.topright), (self.FieldRect.bottomright), 1)
          #pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.midtop), (self.FieldRect.midbottom), 3)
          #pygame.draw.circle(self.FieldSfce, SNOW, (self.FieldRect.centerx+1, self.FieldRect.centery+1), FIELD_CENTER_SIZE, 3)

          pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.left+NET_SIZE, self.FieldRect.top), (self.FieldRect.left+NET_SIZE, self.FieldRect.bottom), 5) 
          pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.right-NET_SIZE, self.FieldRect.top), (self.FieldRect.right-NET_SIZE,self.FieldRect.bottom), 5) 

          Net(self.FieldSfce, 0, 0, NET_SIZE, FIELD_H)
          Net(self.FieldSfce, FIELD_W - NET_SIZE+1, 0, NET_SIZE, FIELD_H)
          Post(POST_IMAGE, (POST_SIZE, ), (self.FieldRect.right - NET_SIZE, self.FieldRect.top + POST_SIZE/2), POSTS, self.FieldSfce)
          Post(POST_IMAGE, (POST_SIZE, ), (self.FieldRect.left  + NET_SIZE, self.FieldRect.top + POST_SIZE/2), POSTS, self.FieldSfce)
          Post(POST_IMAGE, (POST_SIZE, ), (self.FieldRect.left  + NET_SIZE, self.FieldRect.bottom - POST_SIZE/2), POSTS, self.FieldSfce)
          Post(POST_IMAGE, (POST_SIZE, ), (self.FieldRect.right - NET_SIZE, self.FieldRect.bottom - POST_SIZE/2), POSTS, self.FieldSfce)

          

