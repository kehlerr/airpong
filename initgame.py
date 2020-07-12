import pygame

from common import WINDOW_TITLE, KEY_REPEAT_INT, KEY_REPEAT_DEL
from field import DISPLAY_SIZE, BACKGROUND_COLOR
from battle import Battle


def create_window():
    pygame.time.Clock()
    display = pygame.display.set_mode(DISPLAY_SIZE)
    display.fill(BACKGROUND_COLOR)
    setup_window()
    return display

def setup_window():
    pygame.display.set_caption(WINDOW_TITLE)
    pygame.key.set_repeat(KEY_REPEAT_DEL, KEY_REPEAT_INT)
    pygame.mouse.set_visible(False)

def create_battle():
    window = create_window()
    battle = Battle(window)
    return battle
