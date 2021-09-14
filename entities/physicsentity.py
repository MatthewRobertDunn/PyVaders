
import pymunk
import math
from panda3d.core import CardMaker, NodePath,TransparencyAttrib
#A basic dynamic physics game entity
class PhysicsEntity:
    def __init__(self, context, position = (0,0)):
        self.context = context
        self.loader = context.loader
        self.keys = context.keys
        self.physics_components = []  #contains other physics components, constraints, joints, etc
        self.cardMaker = CardMaker("MapCardMaker") #thing used to make a graphical rectangles.
        self.create_physics_body(position)
        self.create_graphics_model()

        #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.physics_body = pymunk.Body(body_type=pymunk.Body.STATIC)        # Create a Body
        self.physics_body.position = position     # Set the position of the body
        physics_poly = pymunk.Poly.create_box(self.physics_body, (2.0,2.0))
        physics_poly.elasticity = 0.9
        self.physics_components.append(physics_poly)

    #Create the visual component of the game entity
    def create_graphics_model(self):
        self.render_model = self.loader.loadModel("square2.egg")
        texture = self.loader.loadTexture("alien.png")
        self.render_model.setTransparency(TransparencyAttrib.MAlpha, 1)
        self.render_model.setTexture(texture)
        self.update_graphics_model()


    #Creates a rectangle out of polygons, useful for putting sprites on
    def create_card(self,width, height):
        self.cardMaker.setFrame(-(width / 2.0), (width / 2.0), -(height / 2.0), (height / 2.0))
        self.render_model = NodePath(self.cardMaker.generate())

    def load_texture(self, file):
        texture = self.loader.loadTexture(file)
        self.render_model.setTransparency(TransparencyAttrib.MAlpha, 1)
        self.render_model.setTexture(texture)

  #Update graphics model to match the physics model
    def update_graphics_model(self):
        self.render_model.set_pos(self.physics_body.position[0], self.physics_body.position[1], -2.0)
        self.render_model.set_hpr(0,0,math.degrees(-self.physics_body.angle))  # is this right? seems like it
