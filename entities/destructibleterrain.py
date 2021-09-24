import pymunk
from entities.physicsentity import PhysicsEntity
from entities.takesdamage import TakesDamage
class DestructibleTerrain(PhysicsEntity, TakesDamage):
    def __init__(self, context, position=(0,0)):
        super().__init__(context, position=position)
        
    def create_physics_body(self, position):
       self.physics_body = pymunk.Body(body_type=pymunk.Body.STATIC)        # Create a Body
       self.physics_body.position = position     # Set the position of the body


    def create_graphics_model(self):
        self.draw.create_card(8.0,8.0)
        self.draw.set_texture_from_file("gfx/asteroid.png")
        lines = self.draw.texture_to_geometry(8.0,8.0,self.draw.texture)

        for line in lines:
            segment = pymunk.Segment(self.physics_body, line[0], line[1], 0.01)  
            segment.collision_type = 1
            segment.entity = self
            self.physics_components.append(segment)
        self.update_graphics_model()
        
    def take_damage(self, source, amount):
        return super().take_damage(source, amount)
