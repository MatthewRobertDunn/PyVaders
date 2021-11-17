from entities.ticking_trait import TickingTrait
from entities.graphics_trait import GraphicsTrait
class SmallExplosion(TickingTrait,GraphicsTrait):
    def __init__(self,*,position, **kwargs):
        super().__init__(**kwargs)
        self.position = position

    def create_graphics_model(self):
        self.draw.create_card(2.0,2.0)
        self.draw.set_texture_from_file("gfx/laserredexplode.png")
        self.draw.set_position(self.position)


    def tick(self):
        self.once_after("die", self.despawn,0.2)  #delete after 1 second
