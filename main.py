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
               if KeyControl.acceleration < 25: KeyControl.acceleration += 2
               if isPressed[K_UP] : initgame.leftSlider.Move(UP, KeyControl.acceleration)
               if isPressed[K_DOWN] : initgame.leftSlider.Move(DOWN, KeyControl.acceleration)
               if isPressed[K_w] : initgame.rightSlider.Move(UP, KeyControl.acceleration)         ####   WTF? O_o It isn't working
               if isPressed[K_s] : initgame.rightSlider.Move(DOWN, KeyControl.acceleration)       ####   

          elif eventKey.type == KEYUP:
               KeyControl.acceleration = 1

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
     
     initgame.ball.Move(initgame.SLIDERS, initgame.POSTS)
#     initgame.ball2.Move(initgame.SLIDERS, initgame.POSTS)
     initgame.rightSlider.Move(random.choice([UP,DOWN]), random.choice(range(5, 10)))


if __name__ == '__main__':
     main()
