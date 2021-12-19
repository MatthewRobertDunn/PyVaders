from entities.physics_trait import PhysicsTrait
from entities.takesdamage_trait import TakesDamageTrait
#A little space invader alien
class Alien(PhysicsTrait, TakesDamageTrait):
    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.create_kinematic_rectangle_body(position, 2.0, 2.9) 

    def on_spawn(self):
        super().on_spawn()
        self.dead_sound = self.context.loader.loadSfx("snd/dead2.wav")

    #Create graphics component
    def create_graphics_model(self):
        self.draw.create_card(2.0,2.0)
        self.draw.set_texture_from_file("gfx/enemyship.png")

    #Die if we take damage
    def take_damage(self, source, amount, contact):
        self.context.score.increase_score(5)
        self.despawn()
        self.dead_sound.play()
