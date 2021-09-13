
import pymunk
import math
from panda3d.core import *
#A basic dynamic physics game entity
class PhysicsEntity:
    def __init__(self, loader, position = (0,0)):
        self.loader = loader
        self.create_physics_body(position)
        self.create_graphics_model()

        #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)        # Create a Body
        self.body.position = position     # Set the position of the body
        self.poly = pymunk.Poly.create_box(self.body, (2.0,2.0))
        self.poly.elasticity = 0.9

    #Create the visual component of the game entity
    def create_graphics_model(self):
        self.model = self.loader.loadModel("square2.egg")
        texture = self.loader.loadTexture("alien.png")
        self.model.setTransparency(TransparencyAttrib.MAlpha, 1)
        self.model.setTexture(texture)
        self.update_graphics_model()

  #Update graphics model to match the physics model
    def update_graphics_model(self):
        self.model.set_pos(self.body.position[0], self.body.position[1], -2.0)
        self.model.set_hpr(0,0,math.degrees(-self.body.angle))  # is this right? seems like it
