class Entity:
    def __init__(self, *, context, **kwargs):
        super().__init__(context=context, **kwargs)
        self.context = context

    def on_spawn(self):
        pass
