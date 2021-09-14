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
    def tick(self, dt):
        rv = self.physics_body.rotation_vector * 20.0  # missile needs more thrust
        print(rv)
        self.physics_body.apply_force_at_local_point((rv[1],rv[0]) ,(0,0)) #-90 degree rotate, missiles go up
        self.update_graphics_model()
