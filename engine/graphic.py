#class that adds drawing capability
from panda3d.core import CardMaker, NodePath,TransparencyAttrib
from panda3d.core import LineSegs
import math
class Graphic:
    cardMaker = CardMaker("MapCardMaker") #thing used to make a graphical rectangles.
    def __init__(self, loader, entity):
        self.entity = entity
        self.loader = loader

        #Creates a rectangle out of polygons, useful for putting sprites on
    def create_card(self,width, height):
        self.cardMaker.setFrame(-(width / 2.0), (width / 2.0), -(height / 2.0), (height / 2.0))
        self.render_model = NodePath(self.cardMaker.generate())

    def load_texture(self, file):
        texture = self.loader.loadTexture(file)
        self.render_model.setTransparency(TransparencyAttrib.MAlpha, 1)
        self.render_model.setTexture(texture)

    #draws an outline of the given physics body using opengl line segs
    def create_debug_shape(self, poly):
        vertices = poly.get_vertices()

        lines = LineSegs()
        for v in range(-1,len(vertices) - 1):
            vx1 = vertices[v]
            vx2 = vertices[v+1]
            lines.moveTo(vx1[0],vx1[1],0)
            lines.drawTo(vx2[0],vx2[1],0)
        lines.setThickness(4)
        node = lines.create()
        self.render_model = NodePath(node)

      #Update graphics model to match the physics model
    def update_graphics_model(self, body):
        self.render_model.set_pos(body.position[0], body.position[1], -2.0)
        self.render_model.set_hpr(0,0,math.degrees(-body.angle))  # is this right? seems like it
