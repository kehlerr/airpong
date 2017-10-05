#!/usr/bin/python 

import pygame, math, numpy,  random, sys
import initgame
from pygame.locals import *
from initgame import *

from functools import wraps


FPS = 60
#DISPLAY_W = 1000
#DISPLAY_H = 600
#DISPLAY_SIZE = (DISPLAY_W, DISPLAY_H)
#FIELD_W = 800
#FIELD_H = 600
#FIELD_CENTER_SIZE = 25
#NET_SIZE = 30
#GOAL_AREA = NET_SIZE
#L_GOAL_LINE = GOAL_AREA
#R_GOAL_LINE = FIELD_W - GOAL_AREA
#NET_DENSE = 25
#CROSS_SIZE = 12



#def initwindow((width, height), title):
     #pygame.init()
#     global CLOCK
#     CLOCK = pygame.time.Clock()

#     display = pygame.display.set_mode((width, height))
#     pygame.display.set_caption(title)
#     display.fill(BKG_CL)
#     pygame.key.set_repeat(50, 5)
     
#     return display


#def initgameobj():
#     global DISPLAYSFCE, FIELD, SLIDERS, SPRITES, leftSlider, rightSlider, ball
#     DISPLAYSFCE = initwindow(DISPLAY_SIZE, 'AirPong')
#     FIELD = Field(DISPLAYSFCE)
#     ball = Ball(DISPLAYSFCE)
     
#     entities = [] 
#     entities.append(ball)
#     SLIDERS = [] 
#     leftSlider  = SliderBate(DISPLAYSFCE, FIELD.FieldRect.left + SLIDER_DISTX, FIELD_H/2)
#     rightSlider = SliderBate(DISPLAYSFCE, FIELD.FieldRect.right - SLIDER_DISTX, FIELD_H/2)
#     entities.append(leftSlider)
#     entities.append(rightSlider)
#     SPRITES = pygame.sprite.RenderPlain(entities)

#class Field:
     
#     def __init__(self, sfce, width = FIELD_W, height = FIELD_H):
#          self.sfce = sfce
#          self.FieldRect = pygame.Rect(0, 0, width, height)
#          self.bkgImg = pygame.image.load('pic/bkg7.jpeg')
#          self.bkgImg = pygame.transform.scale(self.bkgImg, (width, height))
#          self.Draw()

#     def Draw(self):          
#          self.sfce.blit(self.bkgImg, (0, 0))
#          pygame.draw.line(self.sfce, BLACK, (self.FieldRect.topleft), (self.FieldRect.bottomleft), 1)       
#          pygame.draw.line(self.sfce, BLACK, (self.FieldRect.topright), (self.FieldRect.bottomright), 5)
#          pygame.draw.line(self.sfce, SNOW, (self.FieldRect.topright), (self.FieldRect.bottomright), 1)
#          pygame.draw.line(self.sfce, SNOW, (self.FieldRect.midtop), (self.FieldRect.midbottom), 3)      
#          pygame.draw.circle(self.sfce, SNOW, (self.FieldRect.centerx+1, self.FieldRect.centery+1), FIELD_CENTER_SIZE, 3)
#          pygame.draw.line(self.sfce, SNOW, (self.FieldRect.left+NET_SIZE, self.FieldRect.top), (self.FieldRect.left+NET_SIZE, self.FieldRect.bottom), 5) 
#          pygame.draw.line(self.sfce, SNOW, (self.FieldRect.right-NET_SIZE, self.FieldRect.top), (self.FieldRect.right-NET_SIZE,self.FieldRect.bottom), 5) 
#          pygame.draw.circle(self.sfce, SNOW, (self.FieldRect.left+NET_SIZE, self.FieldRect.top+CROSS_SIZE/2), CROSS_SIZE, CROSS_SIZE)
#          pygame.draw.circle(self.sfce, SNOW, (self.FieldRect.left+NET_SIZE, self.FieldRect.bottom-CROSS_SIZE/2), CROSS_SIZE, CROSS_SIZE)
#          pygame.draw.circle(self.sfce, SNOW, (self.FieldRect.right-NET_SIZE, self.FieldRect.top+CROSS_SIZE/2), CROSS_SIZE, CROSS_SIZE)
#          pygame.draw.circle(self.sfce, SNOW, (self.FieldRect.right-NET_SIZE, self.FieldRect.bottom-CROSS_SIZE/2), CROSS_SIZE, CROSS_SIZE)
#          for y in range(FIELD_H / NET_DENSE):
#               pygame.draw.aaline(self.sfce, SNOW, (self.FieldRect.left, y*NET_DENSE), (self.FieldRect.left+NET_SIZE, (y+1)*NET_DENSE), 1) 
#               pygame.draw.aaline(self.sfce, SNOW, (self.FieldRect.left+NET_SIZE, y*NET_DENSE), (self.FieldRect.left, (y+1)*NET_DENSE), 1) 
#               pygame.draw.aaline(self.sfce, SNOW, (self.FieldRect.right, y*NET_DENSE), (self.FieldRect.right-NET_SIZE, (y+1)*NET_DENSE), 1) 
#               pygame.draw.aaline(self.sfce, SNOW, (self.FieldRect.right-NET_SIZE, y*NET_DENSE), (self.FieldRect.right, (y+1)*NET_DENSE), 1) 


def KeyControl(isPressed):

     try:
          if KeyControl.acceleration < 25: KeyControl.acceleration += 2
          if isPressed[K_UP] : initgame.leftSlider.Move(UP, KeyControl.acceleration)
          if isPressed[K_DOWN] : initgame.leftSlider.Move(DOWN, KeyControl.acceleration)
          if isPressed[K_w] : initgame.rightSlider.Move(UP, KeyControl.acceleration)
          if isPressed[K_s] : initgame.rightSlider.Move(DOWN, KeyControl.acceleration)
     except AttributeError:
          KeyControl.acceleration = 1
     except NameError:
          pass     


def main_wrapp(loop):
     @wraps(loop)
     def decorated():
          initgameobj()


          while True:
               initgame.CLOCK.tick(FPS)
               for sprite in initgame.SPRITES:
                    initgame.DISPLAYSFCE.blit(initgame.FIELD.bkgImg, sprite.rect, sprite.rect)
               loop()
               for sprite in initgame.SPRITES:
                    initgame.DISPLAYSFCE.blit(sprite.image, sprite.rect)
               pygame.display.update()
     return decorated          


@main_wrapp
def main():

     for event in pygame.event.get():
          if event.type == QUIT:
               pygame.quit()
               sys.exit()
          if event.type == KEYDOWN:
               KeyControl(pygame.key.get_pressed())
          if event.type == KEYUP:
               KeyControl.acceleration = 2     

     
     initgame.ball.Move(initgame.SLIDERS)
     initgame.rightSlider.Move(random.choice([UP,DOWN]), random.choice(range(5, 10)))


if __name__ == '__main__':
     main()
