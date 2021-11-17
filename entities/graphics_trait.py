from engine.graphic import Graphic
from entities.entity import Entity
class GraphicsTrait(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.draw = Graphic(self.context.loader,self)
        
    def on_spawn(self):
        self.create_graphics_model()
        return super().on_spawn()

    def create_graphics_model(self):
        pass
