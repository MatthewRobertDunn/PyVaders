
from engine.graphic import Graphic
from entities.entity import Entity
import pymunk
#A basic dynamic physics game entity
class PhysicsEntity(Entity):
    def __init__(self, context, position = (0,0)):
        self.keys = context.keys
        self.physics_components = []  #contains other physics components, constraints, joints, etc
        self.context = context
        self.draw = Graphic(context.loader,self)
        self.create_physics_body(position)
        self.create_graphics_model()

        #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.create_static_rectangle_body(position, 2.0, 2.0)

    #Create the visual component of the game entity
    def create_graphics_model(self):
        self.draw.create_card(2.0,2.0)
        self.draw.load_texture("gfx/alien.png")
        self.draw.update_graphics_model()

    def on_collision(self, other, self_contact, other_contact):
        pass

    #returns the default physics polygon
    @property
    def physics_poly(self):
        return self.physics_components[0]

    def create_dynamic_rectangle_body(self,position, width, height, collisions = True):
        self._create_rectangle_body(position,width,height,collisions,pymunk.Body.DYNAMIC)

    def create_static_rectangle_body(self,position, width, height, collisions = True):
        self._create_rectangle_body(position,width,height,collisions,pymunk.Body.STATIC)

    def create_kinematic_rectangle_body(self,position, width, height, collisions = True):
        self._create_rectangle_body(position,width,height,collisions,pymunk.Body.KINEMATIC)

    def _create_rectangle_body(self,position, width, height, collisions, body_type):
        self.physics_body = pymunk.Body(body_type = body_type)        # Create a Body
        self.physics_body.position = position     # Set the position of the body
        physics_poly = pymunk.Poly.create_box(self.physics_body, (width,height))
        physics_poly.density = 1.0
        if collisions:
            physics_poly.collision_type = 1
        physics_poly.entity = self
        self.physics_components.append(physics_poly)
    
    def update_graphics_model(self):
        self.draw.update_graphics_model(self.physics_body)
