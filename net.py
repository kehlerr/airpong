import pygame
from PIL import Image
from field_defs import *
from color_defs import SNOW
import obj_template


class Net(obj_template.T):
    def __init__(self, spr_img, size, pos, sfce, crop_rect):
        obj_template.T.__init__(self, spr_img, size, pos, sfce=sfce, crop_rect=crop_rect)
'''
            for y in range(FIELD_H / NET_DENSE):
                pygame.draw.aaline(self.sfce, SNOW, (pos_x, y*NET_DENSE), (pos_x+NET_SIZE, (y+1)*NET_DENSE), 1)
                pygame.draw.aaline(self.sfce, SNOW, (pos_x+NET_SIZE, y*NET_DENSE), (pos_x, (y+1)*NET_DENSE), 1)
'''