
import pymunk
import math
from panda3d.core import CardMaker, NodePath,TransparencyAttrib
#A basic dynamic physics game entity
class PhysicsEntity:
    cardMaker = CardMaker("MapCardMaker") #thing used to make a graphical rectangles.
    def __init__(self, context, position = (0,0)):
        self.context = context
        self.loader = context.loader
        self.keys = context.keys
        self.physics_components = []  #contains other physics components, constraints, joints, etc
        self.create_physics_body(position)
        self.create_graphics_model()

        #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.create_static_rectangle_body(position, 2.0, 2.0)

    #Create the visual component of the game entity
    def create_graphics_model(self):
        #self.render_model = self.loader.loadModel("square2.egg")
        self.create_card(2.0,2.0)
        self.load_texture("gfx/alien.png")
        self.update_graphics_model()


    def on_collision(self, other):
        pass

    #Creates a rectangle out of polygons, useful for putting sprites on
    def create_card(self,width, height):
        self.cardMaker.setFrame(-(width / 2.0), (width / 2.0), -(height / 2.0), (height / 2.0))
        self.render_model = NodePath(self.cardMaker.generate())

    def load_texture(self, file):
        texture = self.loader.loadTexture(file)
        self.render_model.setTransparency(TransparencyAttrib.MAlpha, 1)
        self.render_model.setTexture(texture)


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

  #Update graphics model to match the physics model
    def update_graphics_model(self):
        self.render_model.set_pos(self.physics_body.position[0], self.physics_body.position[1], -2.0)
        self.render_model.set_hpr(0,0,math.degrees(-self.physics_body.angle))  # is this right? seems like it
