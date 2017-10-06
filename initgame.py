#!/usr/bin/python

import pygame
from field  import *
from slider import *
from ball   import *

def initwindow((width, height), title):
     #pygame.init()
     global CLOCK
     CLOCK = pygame.time.Clock()

     display = pygame.display.set_mode((width, height))
     pygame.display.set_caption(title)
     display.fill(BKG_CL)
     pygame.key.set_repeat(50, 5)
                                        
     return display


def initgameobj():
     global DISPLAYSFCE, FIELD, SPRITES, leftSlider, rightSlider, ball
     DISPLAYSFCE = initwindow(DISPLAY_SIZE, 'AirPong')
     FIELD = Field(DISPLAYSFCE)
     ball = Ball(DISPLAYSFCE)
                                                                      
     entities = [] 
     entities.append(ball)
     SLIDERS = [] 
     leftSlider  = SliderBate(DISPLAYSFCE, FIELD.FieldRect.left + SLIDER_DISTX, FIELD_H/2)
     rightSlider = SliderBate(DISPLAYSFCE, FIELD.FieldRect.right - SLIDER_DISTX, FIELD_H/2)

     entities.append(leftSlider)
     entities.append(rightSlider)
     SPRITES = pygame.sprite.RenderPlain(entities)
