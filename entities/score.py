from entities.graphics_trait import GraphicsTrait
from direct.gui.OnscreenText import OnscreenText


class Score(GraphicsTrait):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.context.increase_score = self.increase_score

    def create_graphics_model(self):
        text = OnscreenText(text='my text string', pos=(0, 0), scale=2.5)
        text.setFg((1,1,1,1))
        text.set_pos(0,22,-1)
        text.setText(str(self.score))
        self.text = text
        self.draw.render_model = text

    def increase_score(self,amount):
        self.score += amount
        self.text.setText(str(self.score))
