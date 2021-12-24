from entities.entity import Entity
import random
#An entity that receives ticks
class TickingTrait(Entity):
    delta_time = 0.0        #Time passed per frame, secs
    time = 0.0      #time passed since simulation start, secs
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.at_most_funcs = {}
        self.after_funcs = {}

    #Main game logic
    def tick(self):
        pass

    def update_graphics_model(self):
        pass

    #Rate limits a function to at most time seconds
    def at_most(self, task_name, func, limit):
        if(TickingTrait.time - self.at_most_funcs.get(task_name, -limit) >= limit):
            func()
            self.at_most_funcs[task_name] = TickingTrait.time   #We last fired this func now

    def chance(self, chance, func):
        if random.random() < chance:
            func()

    def once(self, task_name, func):
        self.once_after(task_name,func,0)

    #Runs a function once after a length of time has passed
    def once_after(self,task_name, func, limit):
        fireTime = self.after_funcs.get(task_name, None)
        if fireTime is None:
            self.after_funcs[task_name] = self.time + limit
            return
        elif self.time >= fireTime:
            func()  #fire it
            self.after_funcs[task_name] = float('inf')
