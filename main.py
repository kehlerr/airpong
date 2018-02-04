#!/usr/bin/python 

import pygame, random
from functools import wraps
from sys       import exit
from pygame.locals import *

import initgame
from initgame import *


def KeyControl(eventKey):
     try:
          if eventKey.type == KEYDOWN:
               isPressed = pygame.key.get_pressed()
               if KeyControl.acceleration < 10: KeyControl.acceleration += 0.5
               if isPressed[K_UP]: initgame.BOTSLIDER.Move(UP, KeyControl.acceleration)
               if isPressed[K_DOWN]: initgame.BOTSLIDER.Move(DOWN, KeyControl.acceleration)
               if isPressed[K_w]: initgame.USERSLIDER.Move(UP, KeyControl.acceleration)
               if isPressed[K_s]: initgame.USERSLIDER.Move(DOWN, KeyControl.acceleration)

          elif eventKey.type == KEYUP:
               KeyControl.acceleration = 1

          elif eventKey.type == MOUSEMOTION:
               initgame.USERSLIDER.rect.y = pygame.mouse.get_pos()[Y]

     except AttributeError:
          KeyControl.acceleration = 1
     except NameError:
          pass     


def main_wrapp(loop):
     @wraps(loop)
     def decorated():
          initgameobj()

          while True:
               CLOCK.tick(FPS)
               for sprite in initgame.SPRITES:
                    initgame.DISPLAYSFCE.blit(initgame.FIELD.FieldSfce, sprite.rect, sprite.rect)

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
               exit()
          else:
               KeyControl(event)
               KeyControl(event)

     for ball in initgame.BALLS:
          ball.Live(initgame.SLIDERS.sprites(), initgame.POSTS.sprites())

     initgame.SPRITES.add(initgame.SPARKLES)


if __name__ == '__main__':
     main()
