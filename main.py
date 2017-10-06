#!/usr/bin/python 

import pygame, math, numpy,  random, sys
from functools import wraps
from pygame.locals import *

import initgame
from initgame import *



FPS = 60

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
