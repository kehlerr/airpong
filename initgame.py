import pygame

from common import WINDOW_TITLE, DISPLAY_SIZE,\
    KEY_REPEAT_INTERVAL, KEY_REPEAT_DELAY
from field import BACKGROUND_COLOR
from battle import Battle


def create_window():
    pygame.time.Clock()
    display = pygame.display.set_mode(DISPLAY_SIZE)
    display.fill(BACKGROUND_COLOR)
    setup_window()
    return display

def setup_window():
    pygame.display.set_caption(WINDOW_TITLE)
    pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
    pygame.mouse.set_visible(False)

def create_battle():
    window = create_window()
    battle = Battle(window)
    return battle
