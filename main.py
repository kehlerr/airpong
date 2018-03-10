#!/usr/bin/python 

from functools import wraps
from sys import exit

from pygame.locals import *

import initgame
from common import *


def main_wrapp(loop):
    global battle
    battle = initgame.initgame()

    @wraps(loop)
    def decorated():
        while True:
            battle.update(loop, CLOCK.tick(FPS))
    return decorated


@main_wrapp
def main():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        else:
            battle.handle_event(event)


if __name__ == '__main__':
    main()
