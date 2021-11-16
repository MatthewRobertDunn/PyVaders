from pymunk.vec2d import Vec2d
from entities.alien import Alien
from entities.ticking_trait import TickingTrait
class AlienWave(TickingTrait):

    def on_spawn(self):
        self.aliens=[]
        self.direction = Vec2d(1,0)
        self.new_direction = Vec2d(1,0)

        columns = 10
        rows = 3
        left = -15
        top = 15
        width = 3
        height = 3

        for x in range(0,columns):
            for y in range(0,rows):
                alien = Alien(context=self.context, position=(left + x*width,top + y*height))
                self.context.spawn_entity(alien)
                self.aliens.append(alien)

        self.initial_count = len(self.aliens)

    def tick(self):
        percent_left = len(self.aliens) / self.initial_count 
        self.at_most("move_wave",self.move_wave, 0.05 + 0.25 * percent_left)

    
    def move_wave(self):
        self.direction = self.new_direction
        move_down = False
        self.aliens = [x for x in self.aliens if x.is_alive]
        for alien in self.aliens:
            old_position = alien.physics_body.position
            new_position = old_position + self.direction
            if(new_position[0] > 30 or new_position[0] < -30):
                self.new_direction = self.direction * -1
                move_down = True
            alien.physics_body.position = new_position
            alien.update_graphics_model()

        if move_down:
            self.move_down()

    def move_down(self):
        for alien in [x for x in self.aliens if x.is_alive]:
            old_position = alien.physics_body.position
            new_position = old_position + (0,-1)
            alien.physics_body.position = new_position
            alien.update_graphics_model()
