class Animation:
    def __init__(self):
        self.objects = []
        self.workers = []

    def add(self, obj):
        self.objects.append(obj)

    def add_worker(self, f):
        self.workers.append(f)

    def update(self, dt):
        for obj in self.objects:
            if not obj or not obj.process(dt):
                self.objects.remove(obj)

        for wrk in self.workers:
            if not wrk(dt):
                self.workers.remove(wrk)
