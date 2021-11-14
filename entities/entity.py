class Entity:
    def __init__(self, *, context, **kwargs):
        self.context = context

    def on_spawn(self):
        pass
