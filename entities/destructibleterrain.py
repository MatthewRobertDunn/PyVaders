from entities.entity import Entity
import pymunk
from entities.physicsentity import PhysicsEntity
from entities.takesdamage import TakesDamage
class DestructibleTerrain(PhysicsEntity, TakesDamage):
    def __init__(self,*, context, position=(0,0), **kwargs):
        super().__init__(context=context, position=position, **kwargs)
        
    def create_physics_body(self, position):
       self.physics_body = pymunk.Body(body_type=pymunk.Body.STATIC)        # Create a Body
       self.physics_body.position = position     # Set the position of the body
    
    BODY_WIDTH = 8.0
    BODY_HEIGHT = 12.0

    def create_graphics_model(self):
        self.draw.create_card(self.BODY_WIDTH,self.BODY_HEIGHT)
        #self.draw.set_texture_from_file("gfx/asteroid.png")
        self.draw.set_texture_from_file("gfx/asteroid.png")
        self.hole_image = self.draw.load_image("gfx/hole.png")
        self.physics_components = self.get_segments()
        self.update_graphics_model()
        
    def take_damage(self, source, amount, self_contact):
        text_coord = self.draw.model_coord_to_texture_coord(self_contact,self.BODY_WIDTH,self.BODY_HEIGHT)
        self.draw.mult_image(self.hole_image, text_coord)
        #Get new physics segments
        new_segments = self.get_segments()
        if len(new_segments) == 0:
            self.context.despawn_entity(self) #no physics segments, kill me.
        else:
            self.context.replace_physics_components(self,new_segments)

    def get_segments(self):
        segments = []
        lines = self.draw.texture_to_geometry(self.BODY_WIDTH,self.BODY_HEIGHT,self.draw.texture)
        for line in lines:
            segment = pymunk.Segment(self.physics_body, line[0], line[1], 0.01)  
            segment.collision_type = 1
            segment.entity = self
            segments.append(segment)

        return segments
