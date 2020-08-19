from pygame import Surface, Rect, SRCALPHA

from immovable_object import ImmovableObject
from common import X, Y


DIGIT_SIZE = 60, 80
DIGIT_OFFSET = 35, 50


class ScoreBoard(ImmovableObject):
    '''
        Informative and decorative object displaying current game score
    '''
    image_path = 'scoreboard'
    size = 200, 600

    def __init__(self, background_surface, pos):
        super(ScoreBoard, self).__init__(
            background_surface, pos
        )
        self.score = None
        self.numbers_dest = (self.rect.x+DIGIT_OFFSET[X], self.rect.y+DIGIT_OFFSET[Y])
        numbers_panel_size = self.rect.width - DIGIT_OFFSET[X], DIGIT_SIZE[Y]*2
        self.numbers_rect = Rect(
            (DIGIT_OFFSET[X], DIGIT_OFFSET[Y]),
            numbers_panel_size
        )
        self.surface_copy = Surface(numbers_panel_size, SRCALPHA, 32)
        self.surface_copy.blit(self.surface, ((0,0), numbers_panel_size))
        self.l_number = {}
        self.r_number = {}

    def set_score(self, score):
        self.clear_numbers()
        self.score = score
        self.create_numbers()
        self.redraw()

    def clear_numbers(self):
        '''
            Clear numbers from scoreboard
        '''
        if self.l_number:
            self.del_number(self.l_number)
            self.l_number.clear()
        if self.r_number:
            self.del_number(self.r_number)
            self.r_number.clear()
        self.surface.blit(self.surface_copy, (0, 0))

    def del_number(self, number):
        '''
            Clear number by digits
        '''
        for d in number:
            digit = number[d]
            digit.clear(self.surface)

    def create_numbers(self):
        '''
            Create numbers of score and decompose on digits
        '''
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
                self.surface, (x, y), size, digit, 'red'
            )
            x += DIGIT_OFFSET[X]/l_digits_count

        digit_width = DIGIT_SIZE[X]*(r_digits_count-1)/(r_digits_count**2+2)
        x = self.rect.width/2 + DIGIT_OFFSET[X] - digit_width
        for digit in r_num:
            size = (DIGIT_SIZE[X] / scale, DIGIT_SIZE[Y] / scale)
            self.r_number[digit] = Digit(
                self.surface, (x, y), size, digit, 'blue'
            )
            x += DIGIT_OFFSET[X]/r_digits_count

    def redraw(self):
        self.background_surface.blit(
            self.surface,
            self.numbers_dest, self.numbers_rect
        )


class Digit(ImmovableObject):
    '''
        Static digit image displaying on scoreboard
    '''

    def __init__(self, background_surface, pos, size, digit, color):
        image_path = f'digit_{digit}_{color}'
        super(Digit, self).__init__(
            background_surface, pos, image_path, size = size
        )
