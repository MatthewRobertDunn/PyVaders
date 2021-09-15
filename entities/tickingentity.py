#An entity that receives ticks
class TickingEntity:
    def __init__(self):
        self.at_most_funcs = {}
        self.dt = 0.0
    #Main game logic
    def tick(self):
        raise NotImplementedError()

    def at_most(self, func, limit):
        if(self.at_most_funcs.get(func, limit) >= limit):
            func()
            self.at_most_funcs[func] = 0.0
        else:
            self.at_most_funcs[func] += TickingEntity.dt
