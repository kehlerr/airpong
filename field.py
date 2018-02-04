#!/usr/bin/python

#from field_defs import *
# from color_defs import *
from post import *
from net  import *
from line import *

global POSTS
POSTS = pygame.sprite.Group([])


class Field:
     
    def __init__(self, sfce, width = FIELD_W, height = FIELD_H):
         self.sfce = sfce
         self.FieldSfce = pygame.Surface((width, height))
         self.FieldRect = pygame.Rect(0, 0, width, height)
         self.bkgImg = pygame.image.load('pic/bkg11.jpg')
         self.bkgImg = pygame.transform.scale(self.bkgImg, (width, height))
         self.height = height
         self.width  = width
         self.draw()
         self.bkgImg.blit(self.FieldSfce, (0,0))
         self.sfce.blit(self.bkgImg, (0,0))

    def draw(self):
        self.FieldSfce.blit(self.bkgImg, (0, 0))
        Line(BORDER_TOP_IMG, (0, 0), (self.width, BORDER_HEIGHT), self.FieldSfce)
        Line(BORDER_BOT_IMG, (0, self.height - BORDER_HEIGHT), (self.width, BORDER_HEIGHT), self.FieldSfce)
        Line(CENTER_LINE_IMG, self.FieldRect.center, (0, 0), self.FieldSfce)
        pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.topright), (self.FieldRect.bottomright), 1)
#       pygame.draw.line(self.FieldSfce, SNOW, (self.FieldRect.midtop), (self.FieldRect.midbottom), 3)
#       pygame.draw.circle(self.FieldSfce, SNOW, (self.FieldRect.centerx+1, self.FieldRect.centery+1), FIELD_CENTER_SIZE, 3)
        Line(GOAL_LINE_IMG, (self.FieldRect.left+NET_SIZE, self.FieldRect.centery), (0, 0), self.FieldSfce)
        Line(GOAL_LINE_IMG, (self.FieldRect.right-NET_SIZE, self.FieldRect.centery), (0, 0), self.FieldSfce)
        Net(self.FieldSfce, 0, 0, NET_SIZE, FIELD_H)
        Net(self.FieldSfce, FIELD_W - NET_SIZE+1, 0, NET_SIZE, FIELD_H)
        Post(POST_IMG, (POST_SIZE, ), (self.FieldRect.right - NET_SIZE, self.FieldRect.top + POST_SIZE/2), POSTS, self.FieldSfce)
        Post(POST_IMG, (POST_SIZE, ), (self.FieldRect.left  + NET_SIZE, self.FieldRect.top + POST_SIZE/2), POSTS, self.FieldSfce)
        Post(POST_IMG, (POST_SIZE, ), (self.FieldRect.left  + NET_SIZE, self.FieldRect.bottom - POST_SIZE/2), POSTS, self.FieldSfce)
        Post(POST_IMG, (POST_SIZE, ), (self.FieldRect.right - NET_SIZE, self.FieldRect.bottom - POST_SIZE/2), POSTS, self.FieldSfce)



