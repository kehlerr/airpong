class AnimationController:
    '''
        Class for processing object's animations in a separate cycle
    '''
    def __init__(self):
        self.objects = []

    def add(self, obj):
        '''
            Add object for update
        '''
        self.objects.append(obj)

    def update(self, dt):
        for obj in self.objects:
            if not obj or not obj.process(dt):
                self.objects.remove(obj)