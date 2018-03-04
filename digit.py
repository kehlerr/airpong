#!/usr/bin/python

import obj_template


class Digit(obj_template.T):
    def __init__(self, digit, color, size, pos, sfce):
        spr_img = 'pic/digit_' + digit + '_' + color + '.png'
        obj_template.T.__init__(self, spr_img, size, pos, sfce=sfce)
