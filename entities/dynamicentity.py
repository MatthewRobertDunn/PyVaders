
import pymunk
import math
from entities.physicsentity import PhysicsEntity
from entities.tickingentity import TickingEntity

#A basic dynamic physics game entity
class DynamicEntity(PhysicsEntity, TickingEntity):
    def __init__(self, context, position = (0,0)):
        TickingEntity.__init__(self)
        super().__init__(context,position)
        

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.physics_body = pymunk.Body()        # Create a Body
        self.physics_body.position = position     # Set the position of the body
        physics_poly = pymunk.Poly.create_box(self.physics_body, (2.0,2.0))
        physics_poly.mass = 1.0
        physics_poly.elasticity = 0.5
        self.physics_components.append(physics_poly)

  
    #Main game logic
    def tick(self):
        self.update_graphics_model()
        
