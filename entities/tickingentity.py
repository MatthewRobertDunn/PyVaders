#An entity that receives ticks
class TickingEntity:
    dt = 0.0        #Time passed per frame, secs
    time = 0.0      #time passed since simulation start, secs
    def __init__(self):
        self.at_most_funcs = {}
        
    #Main game logic
    def tick(self):
        raise NotImplementedError()

    def at_most(self, func, limit):
        if(self.at_most_funcs.get(func, limit) >= limit):
            func()
            self.at_most_funcs[func] = 0.0
        else:
            self.at_most_funcs[func] += TickingEntity.dt
