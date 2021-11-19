from engine.graphic import Layers
from entities.graphics_trait import GraphicsTrait
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Material

class Score(GraphicsTrait):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.context.score = self #Add myself to context so other entities can call increase_score

    def create_graphics_model(self):
        text = OnscreenText(text=str(self.score), pos=(0, 0), scale=2.5)
        text.setFg((1,1,1,1))   #white
        text.set_pos(0,21,-1.8)
        text.setText(str(self.score))
        self.text = text
        self.draw.set_node(text, Layers.HUD)

    def increase_score(self,amount):
        self.score += amount
        self.text.setText(str(self.score))
