from base_object import BaseObject


class ImmovableObject(BaseObject):
    def  __init__(self, *args, **kwargs):
        super(ImmovableObject, self).__init__(*args, **kwargs)
        self.draw()