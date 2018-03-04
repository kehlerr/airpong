#!/usr/bin/python

import obj_template
from digit import Digit
from common import *

DIGIT_SIZE = 60, 80
DIGIT_OFFSET = 35, 50


class ScoreBoard(obj_template.T):
    def __init__(self, spr_img, size, pos, sfce):
        obj_template.T.__init__(self, spr_img, size, pos, sfce=sfce)
        self.sb_surface = self.image.copy()
        self.l_number = {}
        self.r_number = {}
        self.numbers_rect = pygame.Rect(DIGIT_OFFSET[X], DIGIT_OFFSET[Y], self.rect.width - 2*DIGIT_OFFSET[X], DIGIT_SIZE[Y])

    def set_score(self, score):
        self.clear()
        l_num = str(score[0])
        r_num = str(score[1])
        scale = max(len(l_num), len(r_num))
        x = self.rect.width/2 - DIGIT_OFFSET[X] - DIGIT_SIZE[X]*(len(l_num)-1)/(len(l_num)**2+1)
        y = self.rect.top + DIGIT_OFFSET[Y] + DIGIT_SIZE[Y] / 2
        for d in l_num:
            self.l_number[d] = Digit(d, 'red', (DIGIT_SIZE[X]/scale, int(DIGIT_SIZE[Y]/scale)), (x, y), sfce=self.sb_surface)
            x += DIGIT_OFFSET[X]/len(l_num)

        x = self.rect.width/2 + DIGIT_OFFSET[X] - DIGIT_SIZE[X]*(len(r_num)-1)/(len(r_num)**2+2)
        for d in r_num:
            self.r_number[d] = Digit(d, 'blue', (DIGIT_SIZE[X]/scale, DIGIT_SIZE[Y]/scale), (x, y), sfce=self.sb_surface)
            x += DIGIT_OFFSET[X]/len(r_num)

        self.sfce.blit(self.sb_surface, (self.rect.x+DIGIT_OFFSET[X], self.rect.y+DIGIT_OFFSET[Y]), self.numbers_rect)

    def clear(self):
        if self.l_number:
            self.del_number(self.l_number)
        if self.r_number:
            self.del_number(self.r_number)

    def del_number(self, number):
        for d in number:
            self.sb_surface.blit(self.image, number[d].rect, number[d].rect)
            number[d].__del__()
