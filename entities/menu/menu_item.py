from direct.gui.OnscreenText import OnscreenText
from engine.graphic import Layers
from entities.graphics_trait import GraphicsTrait
from entities.ticking_trait import TickingTrait

class MenuItem(GraphicsTrait, TickingTrait):
    def __init__(self, *, position, text, on_selected, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.has_focus = False          #does this menu item have focus
        self.on_selected = on_selected  #Function to run on selection of thi item
        self.position = position        #Position

    def set_focus(self, has_focus):
        self.has_focus = has_focus

    def create_graphics_model(self):
        text = OnscreenText(text=str(self.text), pos=(0, 0), scale=2.5)
        text.set_pos(self.position[0],self.position[1],-1.8)
        self.text = text
        self.draw.set_node(text, Layers.HUD)

    def tick(self):
        if(self.has_focus and self.keys.select):
            self.at_most("menu_selected", self.on_selected,0.25)

        if(self.has_focus):
            self.text.setFg((1,1,1,1))   #white
        else:
            self.text.setFg((0.5,0.5,0.5,1))   #grey
