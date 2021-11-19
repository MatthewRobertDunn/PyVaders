#class that adds drawing capability
from panda3d.core import CardMaker, NodePath,TransparencyAttrib
from panda3d.core import LineSegs, PNMImage, Texture
from pymunk.autogeometry import march_soft, simplify_vertexes
from pymunk import BB
#import matplotlib.pyplot as plt
from enum import Enum

class Layers(Enum):
    GAME = 1
    BACKGROUND = 2
    HUD = 3

import math
class Graphic:
    cardMaker = CardMaker("MapCardMaker") #thing used to make a graphical rectangles.

    def __init__(self, loader, entity):
        self.entity = entity
        self.loader = loader
        self.z_order = -2.0
        self.game_node = None
        self.background_node = None
        self.hud_node = None

        #Creates a rectangle out of polygons, useful for putting sprites on
    def create_card(self,width, height, layer = Layers.GAME):
        self.cardMaker.setFrame(-(width / 2.0), (width / 2.0), -(height / 2.0), (height / 2.0))
        node = NodePath(self.cardMaker.generate())
        self._setNode(node, layer)
        return node


    def set_model(self, file, layer = Layers.GAME):
        node = self.loader.loadModel(file)
        self._setNode(node, layer)
        return node

    def set_texture_from_file(self, file, layer = Layers.GAME):
        self.texture = self.load_texture(file)
        self.set_texture(self.texture, layer)

    def set_texture_from_file_no_cache(self, file, layer = Layers.GAME):
        self.texture = self.load_texture_no_cache(file)
        self.set_texture(self.texture, layer)

    def set_texture(self, texture, layer = Layers.GAME):
        node = self._getNode(layer)
        node.setTransparency(TransparencyAttrib.MAlpha, 1)
        node.setTexture(texture)

    def load_texture(self, file):
        return self.loader.load_texture(file)
        
    def load_texture_no_cache(self, file):
        newtex = Texture()
        newtex.setup2dTexture()
        newtex.read(file)
        return newtex

    #draws an outline of the given physics body using opengl line segs
    def create_debug_shape(self, poly, layer = Layers.GAME):
        vertices = poly.get_vertices()
        lines = LineSegs()
        for v in range(-1,len(vertices) - 1):
            vx1 = vertices[v]
            vx2 = vertices[v+1]
            lines.moveTo(vx1[0],vx1[1],0)
            lines.drawTo(vx2[0],vx2[1],0)
        lines.setThickness(4)
        node = NodePath(lines.create())
        self._setNode(node)
        return node

      #Update graphics model to match the physics model
    def update_graphics_model(self, body, layer = Layers.GAME):
        node = self._getNode(layer)
        node.set_pos(body.position[0], body.position[1], self.z_order)
        node.setR(math.degrees(-body.angle))  # is this right? seems like it

    def set_position(self, position, layer = Layers.GAME):
        node = self._getNode(layer)
        node.set_pos(position[0], position[1], self.z_order)

    def texture_to_geometry(self, width, height, texture):
        image = PNMImage()
        texture.store(image)
        bb = BB(-width*0.5, -height*0.5, width*0.5, height*0.5)
        
        xsize = image.getXSize() - 1
        ysize = image.getYSize() - 1
        def sample_func(point):
            x = int((point[0] / width) * xsize  + xsize*0.5)
            y = int(ysize - ((point[1] / height) * ysize + ysize*0.5))
            return 0 if image.getAlphaVal(x,y) == 0 else 1
    
        polylines = march_soft(bb,32,32,0.5,sample_func)

        lines = []

        for poly_line in polylines:
            simple_line = simplify_vertexes(poly_line,0.1)
            for i in range(len(simple_line) - 1):
                a = simple_line[i]
                b = simple_line[i + 1]
                lines.append((a,b))

        #self.debug_draw_lines(lines)        
        return lines

    def _getNode(self, layer):
        if layer == Layers.BACKGROUND:
            return self.background_node
        elif layer == Layers.GAME:
            return self.game_node
        elif layer == Layers.HUD:
            return self.hud_node
        else:
            raise Exception("Invalid layer")

    def _setNode(self, node, layer):
        if layer == Layers.BACKGROUND:
            self.background_node = node
        elif layer == Layers.GAME:
            self.game_node = node
        elif layer == Layers.HUD:
            self.hud_node = node
        else:
            raise Exception("Invalid layer")

    def subtract_image(self, texture_coord, sub_image):
        image = PNMImage()
        self.texture.store(image)
        image.setGreenVal(texture_coord[0],texture_coord[1],255)
        self.texture.load(image)
        self.game_node.setTexture(self.texture)

    def load_image(self, file):
        myImage = PNMImage()
        myImage.read(file)
        return myImage

    def draw_circle(self, texture_coord, d):
        image = PNMImage()
        self.texture.store(image)
        image.setGreenVal(texture_coord[0],texture_coord[1],255)
        self.texture.load(image)
        self.game_node.setTexture(self.texture)

    def mult_image(self, sub_image, texture_coord):
        image = PNMImage()
        self.texture.store(image)
        x_adj = int(sub_image.getXSize() * 0.5)
        y_adj = int(sub_image.getYSize() * 0.5)
        x = texture_coord[0] - x_adj
        y = texture_coord[1] - y_adj
        image.multSubImage(sub_image,x,y,0,0,sub_image.getXSize(),sub_image.getYSize(),1.0)

        self.texture.load(image)
        self.game_node.setTexture(self.texture)


    def model_coord_to_texture_coord(self, model_coord, model_width, model_height):
        xsize = self.texture.getXSize() - 1
        ysize = self.texture.getYSize() - 1
        x = int((model_coord[0] / model_width) * xsize  + xsize*0.5)
        y = int(ysize - ((model_coord[1] / model_height) * ysize + ysize*0.5))
        return (x,y)

    def debug_draw_lines(self,lines):
        for line in lines:
            a = line[0]
            b = line[1]
            plt.plot([a[0],b[0]],[a[1],b[1]], marker = 'o')
        plt.show()
