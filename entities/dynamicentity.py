
import pymunk
import math
from entities.physicsentity import PhysicsEntity
from entities.tickingentity import TickingEntity

#A basic dynamic physics game entity
class DynamicEntity(PhysicsEntity, TickingEntity):
    def __init__(self, loader, position = (0,0)):
        super().__init__(loader,position)

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.body = pymunk.Body()        # Create a Body
        self.body.position = position     # Set the position of the body
        self.poly = pymunk.Poly.create_box(self.body, (2.0,2.0))
        self.poly.mass = 1.0
        self.poly.elasticity = 0.5

  
    #Main game logic
    def tick(self, dt):
        self.update_graphics_model()
        
