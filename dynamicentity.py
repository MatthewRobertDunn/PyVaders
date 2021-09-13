
import pymunk

#A basic dynamic physics game entity
class DynamicEntity:
    def __init__(self, loader, position = (0,0)):
        self.loader = loader
        self.create_physics_body(position)
        self.create_graphics_model()

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.body = pymunk.Body()        # Create a Body
        self.body.position = position     # Set the position of the body
        self.poly = pymunk.Poly.create_box(self.body, (1.0,1.0))
        self.poly.mass = 1.0

    #Create the visual component of the game entity
    def create_graphics_model(self):
        self.model = self.loader.loadModel("square2.egg")
        self.update_graphics_model()

    #Update graphics model to match the physics model
    def update_graphics_model(self):
        self.model.set_pos(self.body.position[0], self.body.position[1], -2.0)
        #todo set graphics model rotation based on physics body rotation?

    #Main game logic
    def tick(self, dt):
        self.update_graphics_model()
        
