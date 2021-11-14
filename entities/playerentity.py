
import pymunk
import math
from panda3d.core import CardMaker, NodePath,TransparencyAttrib
from entities.dynamicentity import DynamicEntity
from entities.missile import Missile
#A basic dynamic physics game entity
class PlayerEntity(DynamicEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.create_dynamic_rectangle_body(position, 4.0, 3.0)
        move_joint = pymunk.GrooveJoint(self.context.static_body, self.physics_body, (-100, position[1]), (100, position[1]), (0, 0))
        self.physics_components.append(move_joint)

    def create_graphics_model(self):
        self.draw.create_card(5.0,5.0)  #Create a 5x5 card
        self.draw.set_texture_from_file("gfx/p38_lvl_3_d4.png")
        #self.draw.create_debug_shape(self.physics_poly)

    #Main game logic
    def tick(self):
        if self.keys.right:
            self.physics_body.apply_force_at_local_point((500.0,0.0),(0,0))
        
        if self.keys.left:
            self.physics_body.apply_force_at_local_point((-500.0,0.0),(0,0))

        if self.keys.fire:
            self.at_most("fire_missile", self.fire_missile,0.25)    
        
    def fire_missile(self):
        missile = Missile(context = self.context,position = (self.physics_body.position[0], self.physics_body.position[1]+2.5))
        missile.physics_body.velocity = self.physics_body.velocity
        self.context.spawn_entity(missile)
