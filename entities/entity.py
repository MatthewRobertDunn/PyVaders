class Entity:
    def __init__(self, *, context, **kwargs):
        self.context = context

    def despawn(self):
        self.context.despawn_entity(self)

    def on_spawn(self):
        pass
