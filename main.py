#!/usr/bin/python3.7

from functools import wraps
from sys import exit

import pygame
from pygame.locals import QUIT

import initgame
from common import CLOCK, FPS


def main_wrapper(loop):
    @wraps(loop)
    def decorated():
        battle = initgame.create_battle()
        context = { 'battle': battle }
        loop(context = context)
    return decorated

@main_wrapper
def main_loop(context = {}):
    try:
        battle = context.get('battle')
        while True:
            battle.update(handle_events, CLOCK.tick(FPS))
    except KeyboardInterrupt:
        pygame.quit()

def handle_events(handler):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        handler.handle_event(event)

if __name__ == '__main__':
    main_loop()
