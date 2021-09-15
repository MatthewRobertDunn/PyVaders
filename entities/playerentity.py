
import pymunk
import math
from panda3d.core import CardMaker, NodePath,TransparencyAttrib
from entities.dynamicentity import DynamicEntity
from entities.missile import Missile
#A basic dynamic physics game entity
class PlayerEntity(DynamicEntity):
    def __init__(self, context, position = (0,0)):
        super().__init__(context,position)

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.create_dynamic_rectangle_body(position, 4.0, 3.0)
        move_joint = pymunk.GrooveJoint(self.context.static_body, self.physics_body, (-100, position[1]), (100, position[1]), (0, 0))
        self.physics_components.append(move_joint)

    def create_graphics_model(self):
        self.create_card(5.0,5.0)  #Create a 5x5 card
        self.load_texture("gfx/p38_lvl_3_d4.png")

    #Main game logic
    def tick(self):
        self.update_graphics_model()
        if self.keys.right:
            self.physics_body.apply_force_at_local_point((500.0,0.0),(0,0))
        
        if self.keys.left:
            self.physics_body.apply_force_at_local_point((-500.0,0.0),(0,0))

        if self.keys.fire:
            self.at_most("fire_missile", self.fire_missile,1.0)    
        
    def fire_missile(self):
        missile = Missile(self.context,(self.physics_body.position[0], self.physics_body.position[1]+2.5))
        self.context.spawn_entity(missile)
