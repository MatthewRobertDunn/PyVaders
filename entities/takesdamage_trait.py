#Trait you can apply if you wish to be able to receive damage.
from entities.entity import Entity

class TakesDamageTrait(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def take_damage(self, source, amount, self_contact):
        pass
