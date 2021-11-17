class Entity:
    def __init__(self, *, context, **kwargs):
        self.context = context
        self.is_alive = False
        self.keys = self.context.keys

    def despawn(self):
        self.context.despawn_entity(self)

    def on_spawn(self):
        pass
