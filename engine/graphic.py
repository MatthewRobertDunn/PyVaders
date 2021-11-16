#class that adds drawing capability
from panda3d.core import CardMaker, NodePath,TransparencyAttrib
from panda3d.core import LineSegs, PNMImage
from pymunk.autogeometry import march_hard, march_soft, simplify_vertexes
from pymunk import BB, Segment
import matplotlib.pyplot as plt

import math
class Graphic:
    cardMaker = CardMaker("MapCardMaker") #thing used to make a graphical rectangles.
    texture_cache = {}
    def __init__(self, loader, entity):
        self.entity = entity
        self.loader = loader
        

        #Creates a rectangle out of polygons, useful for putting sprites on
    def create_card(self,width, height):
        self.cardMaker.setFrame(-(width / 2.0), (width / 2.0), -(height / 2.0), (height / 2.0))
        self.render_model = NodePath(self.cardMaker.generate())

    def set_texture_from_file(self, file):
        self.texture = self.load_texture_cache(file)
        self.render_model.setTransparency(TransparencyAttrib.MAlpha, 1)
        self.render_model.setTexture(self.texture)
        
    def load_texture_cache(self, file):
        if file in self.texture_cache:
            return self.texture_cache[file]
        else:
            result = self.load_texture(file)
            self.texture_cache[file] = result
            return result
    
    def load_texture(self, file):
        return self.loader.load_texture(file)

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


    def subtract_image(self, texture_coord, sub_image):
        image = PNMImage()
        self.texture.store(image)
        image.setGreenVal(texture_coord[0],texture_coord[1],255)
        self.texture.load(image)
        self.render_model.setTexture(self.texture)

    def load_image(self, file):
        myImage = PNMImage()
        myImage.read(file)
        return myImage

    def draw_circle(self, texture_coord, d):
        image = PNMImage()
        self.texture.store(image)
        image.setGreenVal(texture_coord[0],texture_coord[1],255)
        self.texture.load(image)
        self.render_model.setTexture(self.texture)

    def mult_image(self, sub_image, texture_coord):
        image = PNMImage()
        self.texture.store(image)
        x_adj = int(sub_image.getXSize() * 0.5)
        y_adj = int(sub_image.getYSize() * 0.5)
        x = texture_coord[0] - x_adj
        y = texture_coord[1] - y_adj
        image.multSubImage(sub_image,x,y,0,0,sub_image.getXSize(),sub_image.getYSize(),1.0)

        #image.multSubImage(sub_image,0,0,0,0,sub_image.getXSize(),sub_image.getYSize(),1.0)


        self.texture.load(image)
        self.render_model.setTexture(self.texture)


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
