from entities.tickingentity import TickingEntity
class AlienWave(TickingEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_spawn(self):
        pass
