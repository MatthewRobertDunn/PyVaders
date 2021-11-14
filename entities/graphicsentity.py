from engine.graphic import Graphic
class GraphicsEntity:
    def __init__(self, context, **kwargs):
        super().__init__(**kwargs)
        self.draw = Graphic(context.loader,self)
