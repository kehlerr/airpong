import pygame

from immovable_object import ImmovableObject
from digit import Digit
from common import X, Y


DIGIT_SIZE = 60, 80
DIGIT_OFFSET = 35, 50


class ScoreBoard(ImmovableObject):
    image_path = 'pic/scoreboard.png'
    size = (200, 600)

    def __init__(self, background_surface, pos):
        super(ScoreBoard, self).__init__(
            background_surface, pos
        )
        self.surface_bg = self.image.copy()
        self.score = None
        self.l_number = {}
        self.r_number = {}

    def set_score(self, score):
        self.clear_numbers()
        self.score = score
        self.create_numbers()
        self.redraw()

    def clear_numbers(self):
        if self.l_number:
            self.del_number(self.l_number)
            self.l_number.clear()
        if self.r_number:
            self.del_number(self.r_number)
            self.r_number.clear()

    def del_number(self, number):
        for d in number:
            digit = number[d]
            self.surface_bg.blit(self.surface, digit.rect, digit.rect)

    def create_numbers(self):
        l_num = str(self.score[0])
        r_num = str(self.score[1])

        l_digits_count = len(l_num)
        r_digits_count = len(r_num)

        scale = max(l_digits_count, r_digits_count)
        digit_width = DIGIT_SIZE[X]*(l_digits_count-1)/(l_digits_count**2+1)
        x = self.rect.width/2 - DIGIT_OFFSET[X] - digit_width
        y = self.rect.top + DIGIT_OFFSET[Y] + DIGIT_SIZE[Y] / 2
        for digit in l_num:
            size = (DIGIT_SIZE[X]/scale, int(DIGIT_SIZE[Y]/scale))
            self.l_number[digit] = Digit(
                self.surface_bg, (x, y), size, digit, 'red'
            )
            x += DIGIT_OFFSET[X]/l_digits_count

        digit_width = DIGIT_SIZE[X]*(r_digits_count-1)/(r_digits_count**2+2)
        x = self.rect.width/2 + DIGIT_OFFSET[X] - digit_width
        for digit in r_num:
            size = (DIGIT_SIZE[X] / scale, DIGIT_SIZE[Y] / scale)
            self.r_number[digit] = Digit(
                self.surface_bg, (x, y), size, digit, 'blue'
            )
            x += DIGIT_OFFSET[X]/r_digits_count

    def redraw(self):
        dest = (self.rect.x+DIGIT_OFFSET[X], self.rect.y+DIGIT_OFFSET[Y])
        numbers_rect = pygame.Rect(
            DIGIT_OFFSET[X], DIGIT_OFFSET[Y],
            self.rect.width - 2*DIGIT_OFFSET[X], DIGIT_SIZE[Y]
        )
        self.background_surface.blit(self.surface_bg, dest, numbers_rect)
        pygame.display.update(self.rect)
