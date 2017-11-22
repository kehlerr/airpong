#!/usr/bin/python

from oth     import *
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


def initgameobj():
     global DISPLAYSFCE, FIELD, SPRITES, USERSLIDER, BOTSLIDER

     DISPLAYSFCE = initwindow(DISPLAY_SIZE, WINDOW_TITLE)
     FIELD = Field(DISPLAYSFCE)

     Ball(FIELD.FieldSfce, FIELD.FieldSfce)
     USERSLIDER = Slider(FIELD.FieldSfce, L_GOAL_LINE + SLIDER_DISTX, 10, 'pic/slider_red.png')
     BOTSLIDER = Slider(FIELD.FieldSfce, R_GOAL_LINE - SLIDER_DISTX,  10, 'pic/slider_blue.png')
    
     SPRITES = pygame.sprite.RenderPlain(BALLS, SLIDERS)

