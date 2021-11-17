import pymunk

from entities.dynamic_trait import DynamicTrait
from entities.small_explosion import SmallExplosion
from entities.takesdamage_trait import TakesDamageTrait
#A basic missile entity
class Missile(DynamicTrait):
    def __init__(self, *, velocity, **kwargs):
        super().__init__(**kwargs)
        self.velocity = velocity

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.create_dynamic_rectangle_body(position, 0.25, 1.0)     #Missiles are narrow and long
        self.physics_body.velocity = self.velocity
        del self.velocity

    def create_graphics_model(self):
        self.draw.create_card(0.25,2.0)  #Create a 5x5 card
        self.draw.set_texture_from_file("gfx/laserred.png")

    #Main game logic
    def tick(self):
        self.physics_body.apply_force_at_local_point(force=(0.0,30.0),point=(0,0))
        self.once_after("explode", self.explode,5.0)  #delete rocket after 1 second
        

    def on_collision(self, other, self_contact, other_contact):
        if isinstance(other,TakesDamageTrait):
            other.take_damage(self,10.0, self_contact)    #Cause 10 damage
        self.explode()

    def explode(self):
        #No explosion yet
        self.context.spawn_entity(SmallExplosion(position=self.physics_body.position,context=self.context))
        self.despawn()
