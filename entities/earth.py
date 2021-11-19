from engine.graphic import Layers
from entities.ticking_trait import TickingTrait
from entities.graphics_trait import GraphicsTrait
class Earth(TickingTrait,GraphicsTrait):
    def create_graphics_model(self):
        node = self.draw.set_model("gfx/earth/scene.gltf",Layers.BACKGROUND)
        node.setScale(0.01)
        node.setPos(0, 0, -100)

    def tick(self):
        #slowly rotate the planet
        self.draw.background_node.setHpr(0,TickingTrait.time,90)
