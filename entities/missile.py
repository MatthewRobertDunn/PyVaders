import pymunk
from entities.dynamicentity import DynamicEntity
#A basic missile entity
class Missile(DynamicEntity):
    def __init__(self, context, position = (0,0)):
        super().__init__(context,position)

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.create_dynamic_rectangle_body(position, 0.25, 1.0)     #Missiles are narrow and long

    def create_graphics_model(self):
        self.create_card(0.25,1.0)  #Create a 5x5 card

    #Main game logic
    def tick(self):
        self.physics_body.apply_force_at_local_point(force=(0.0,10.0),point=(0,0))
        self.update_graphics_model()
