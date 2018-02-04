#!/usr/bin/python

from common     import *
from field   import *
from slider  import *
from ball    import *

def initwindow((width, height), title):
     #pygame.init()
     CLOCK = pygame.time.Clock()

     display = pygame.display.set_mode((width, height))
     pygame.display.set_caption(title)
     display.fill(BKG_CL)
     pygame.key.set_repeat(KEY_REPEAT_DEL, KEY_REPEAT_INT)
     pygame.mouse.set_visible(False)
                                        
     return display


SLIDERS = pygame.sprite.Group([])
BALLS = pygame.sprite.Group([])

def initgameobj():
     global DISPLAYSFCE, FIELD, SPRITES, USERSLIDER, BOTSLIDER


     DISPLAYSFCE = initwindow(DISPLAY_SIZE, WINDOW_TITLE)
     FIELD = Field(DISPLAYSFCE)

     Ball('pic/ball_blue.png', FIELD.FieldSfce, (440,330), BALLS)
     USERSLIDER = Slider('pic/slider_red.png', (SLIDER_W, SLIDER_H), (L_GOAL_LINE + SLIDER_DISTX, 100), SLIDERS)
     BOTSLIDER = Slider('pic/slider_blue.png', (SLIDER_W, SLIDER_H), (R_GOAL_LINE - SLIDER_DISTX, 100), SLIDERS)

     SPRITES = pygame.sprite.RenderPlain(BALLS, SLIDERS)

