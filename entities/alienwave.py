from pymunk.vec2d import Vec2d
from entities.alien import Alien
from entities.big_message import BigMessage
from entities.ticking_trait import TickingTrait
import itertools
class AlienWave(TickingTrait):

    def on_spawn(self):
        self.aliens=[]
        self.direction = Vec2d(1,0)
        self.new_direction = Vec2d(1,0)

        columns = 15
        rows = 5
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
        remaining = len(self.aliens)
        if(remaining == 0):
            self.despawn()
            self.game_won()
            return

        percent_left = remaining / self.initial_count 
        self.at_most("move_wave",self.move_wave, 0.01 + 0.25 * percent_left)
        self.at_most("aliens_shoot",self.alien_shoot,1.0)

    def alien_shoot(self):
        #Group aliens by X coordinate
        candidates = []
        for key, column in itertools.groupby(self.aliens, lambda alien: alien.physics_body.position[0]):
            lowest_alien = min(column, key=lambda alien: alien.physics_body.position[1])
            candidates.append(lowest_alien)
        
        for alien in candidates:
            self.chance(1.0 / len(candidates), alien.fire)

    def move_wave(self):
        self.direction = self.new_direction
        move_down = False
        self.aliens = [x for x in self.aliens if x.is_alive]

        for alien in self.aliens:
            old_position = alien.physics_body.position
            new_position = old_position + self.direction
            if(new_position[0] > 38 or new_position[0] < -38):
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

    def game_won(self):
        entity = BigMessage(context = self.context, text="You Won!")
        self.context.spawn_entity(entity)
