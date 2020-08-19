import os
from pygame import time, image

CLOCK = time.Clock()
FPS = 60
KEY_REPEAT_DELAY = 10
KEY_REPEAT_INTERVAL = 12
WINDOW_TITLE = 'AirPong'
DISPLAY_W = 1000
DISPLAY_H = 600
DISPLAY_SIZE = (DISPLAY_W, DISPLAY_H)

X = 0
Y = 1

DOWN = -1
UP = 1

IMAGES_FOLDER_PATH = 'pic/'
IMAGE_EXT = '.png'

def load_image(image_name):
    '''
        Common way to load every sprite
    '''
    image_path = os.path.join(IMAGES_FOLDER_PATH, image_name+IMAGE_EXT)
    return image.load(image_path)
