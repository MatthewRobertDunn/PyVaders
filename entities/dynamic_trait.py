
import pymunk
import math
from entities.physics_trait import PhysicsTrait
from entities.ticking_trait import TickingTrait

#A basic dynamic physics game entity
class DynamicTrait(PhysicsTrait, TickingTrait):
    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.physics_body = pymunk.Body()        # Create a Body
        self.physics_body.position = position     # Set the position of the body
        physics_poly = pymunk.Poly.create_box(self.physics_body, (2.0,2.0))
        physics_poly.mass = 1.0
        physics_poly.elasticity = 0.5
        self.physics_components.append(physics_poly)
        
