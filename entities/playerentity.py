
import pymunk
import math
from panda3d.core import CardMaker, NodePath,TransparencyAttrib
from entities.dynamicentity import DynamicEntity
#A basic dynamic physics game entity
class PlayerEntity(DynamicEntity):
    def __init__(self, context, position = (0,0)):
        super().__init__(context,position)

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.physics_body = pymunk.Body()        # Create a Body
        self.physics_body.position = position     # Set the position of the body
        physics_poly = pymunk.Poly.create_box(self.physics_body, (4.0,3.0))
        physics_poly.mass = 1.0
        physics_poly.elasticity = 0.5
        self.physics_components.append(physics_poly)

        move_joint = pymunk.GrooveJoint(self.context.static_body, self.physics_body, (-100, position[1]), (100, position[1]), (0, 0))
        self.physics_components.append(move_joint)

  

    def create_graphics_model(self):
        # Make a card on which the shader will render the map
        c = CardMaker("MapCardMaker")
        c.setFrame(-2.5, 2.5, -2.5, 2.5)
        self.render_model = NodePath(c.generate())
        #self.render_model.setColor(1.0,1.0,0.0)
        texture = self.loader.loadTexture("gfx/p38_lvl_3_d4.png")
        self.render_model.setTransparency(TransparencyAttrib.MAlpha, 1)
        self.render_model.setTexture(texture)

        self.update_graphics_model()

    #Main game logic
    def tick(self, dt):
        self.update_graphics_model()
        if self.keys.right:
            self.physics_body.apply_force_at_local_point((50.0,0.0),(0,0))
        
        if self.keys.left:
            self.physics_body.apply_force_at_local_point((-50.0,0.0),(0,0))
        
        
        
