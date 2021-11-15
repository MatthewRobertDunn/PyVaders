import pymunk

from entities.dynamic_trait import DynamicTrait
from entities.takesdamage_trait import TakesDamageTrait
#A basic missile entity
class Missile(DynamicTrait):
    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.create_dynamic_rectangle_body(position, 0.25, 1.0)     #Missiles are narrow and long

    def create_graphics_model(self):
        self.draw.create_card(1.0,1.0)  #Create a 5x5 card
        self.draw.set_texture_from_file("gfx/missile00.png")

    #Main game logic
    def tick(self):
        self.physics_body.apply_force_at_local_point(force=(0.0,30.0),point=(0,0))
        self.once_after("explode", self.explode,5.0)  #delete rocket after 1 second
        

    def on_collision(self, other, self_contact, other_contact):
        if isinstance(other,TakesDamageTrait):
            other.take_damage(self,10.0, other_contact)    #Cause 10 damage
        self.explode()

    def explode(self):
        #No explosion yet
        self.despawn()
