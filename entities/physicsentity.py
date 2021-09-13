
import pymunk
import math

#A basic dynamic physics game entity
class PhysicsEntity:
    def __init__(self, loader, position = (0,0)):
        self.loader = loader
        self.create_physics_body(position)
        self.create_graphics_model()

        #Create the physics component of the game entity.
    def create_physics_body(self, position):
        raise NotImplementedError()

    #Create the visual component of the game entity
    def create_graphics_model(self):
        self.model = self.loader.loadModel("square2.egg")
        self.update_graphics_model()

  #Update graphics model to match the physics model
    def update_graphics_model(self):
        self.model.set_pos(self.body.position[0], self.body.position[1], -2.0)
        self.model.set_hpr(0,0,math.degrees(-self.body.angle))  # is this right? seems like it
