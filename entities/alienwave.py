from entities.entity import Entity
from entities.ticking_trait import TickingTrait
class AlienWave(TickingTrait):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_spawn(self):
        pass
