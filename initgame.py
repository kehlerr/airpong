#!/usr/bin/python

from common import *
from color_defs import *
from field_defs import *
import battle


def initwindow((width, height), title):
     #pygame.init()
    CLOCK = pygame.time.Clock()
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    display.fill(BKG_CL)
    pygame.key.set_repeat(KEY_REPEAT_DEL, KEY_REPEAT_INT)
    pygame.mouse.set_visible(False)

    return display


def initgame():
    return battle.Battle(initwindow(DISPLAY_SIZE, WINDOW_TITLE))

