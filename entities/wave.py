from entities.tickingentity import TickingEntity
from entities.alien import Alien
class AlienWave(TickingEntity):
    def  __init__(self):
        self.aliens = []
        super().__init__()

    
    def on_spawn(self):
        for x in range(-25,25,3):
            for y in range(12,24,4):
                entity = Alien(self.context,(x,y))      
                self.aliens.append(entity)
                self.context.spawn_entity(entity)
