from immovable_object import ImmovableObject


class Digit(ImmovableObject):
    def __init__(self, background_surface, pos, size, digit, color):
        image_path = f'digit_{digit}_{color}'
        super(Digit, self).__init__(
            background_surface, pos, image_path, size = size
        )
