from entities.dynamicentity import DynamicEntity
from entities.takesdamage import TakesDamage
#A little space invader alien
class Alien(DynamicEntity, TakesDamage):
    def __init__(self, context, position = (0,0)):
        super().__init__(context,position)

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.create_kinematic_rectangle_body(position, 2.0, 1.9)     #Missiles are narrow and long

    def create_graphics_model(self):
        self.draw.create_card(2.0,2.0)  #Create a 5x5 card
        self.draw.set_texture_from_file("gfx/alien.png")

    def take_damage(self, source, amount, contact):
        self.despawn()

    #Main game logic
    def tick(self):
        pass
        
