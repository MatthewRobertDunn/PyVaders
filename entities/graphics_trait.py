from engine.graphic import Graphic
from entities.entity import Entity
class GraphicsTrait(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.draw = Graphic(self.context.loader,self)
