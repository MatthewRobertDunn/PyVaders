
import pymunk
from entities.physicsentity import PhysicsEntity

#A basic dynamic physics game entity
class StaticEntity(PhysicsEntity):
    def __init__(self, loader, position = (0,0)):
        super().__init__(loader,position)

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)        # Create a Body
        self.body.position = position     # Set the position of the body
        self.poly = pymunk.Poly.create_box(self.body, (2.0,2.0))
        self.poly.elasticity = 0.9
