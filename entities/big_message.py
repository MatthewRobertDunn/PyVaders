from engine.graphic import Layers
from entities.graphics_trait import GraphicsTrait
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Material
from entities.ticking_trait import TickingTrait
import random
class BigMessage(GraphicsTrait):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def create_graphics_model(self):
        text_model = OnscreenText(text=self.text, pos=(0, 0), scale=5.5)
        text_model.setFg((1,1,1,1))   #white
        text_model.set_pos(0,5,-1.8)
        self.draw.set_node(text_model, Layers.HUD)
        self.text_model = text_model
        

    def tick(self):
        self.at_most("message_color",self.change_color,0.5)
        return super().tick()

    def change_color(self):
        self.text_model.setFg((random.random(),random.random(),random.random(),1))   #white
