#!/usr/bin/python 

from common import *
from functools import wraps
from sys import exit
from pygame.locals import *

import initgame


def main_wrapp(loop):
    @wraps(loop)
    def decorated():
        while True:
            CLOCK.tick(FPS)
            battle.update(loop)
            pygame.display.update()
    return decorated


@main_wrapp
def main():
    global battle
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        else:
            battle.handle_event(event)

    battle.play()


if __name__ == '__main__':
     battle = initgame.initgame()
     main()
