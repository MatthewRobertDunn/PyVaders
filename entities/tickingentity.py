#An entity that receives ticks
class TickingEntity:
    #Main game logic
    def tick(self, dt):
        raise NotImplementedError()
        
