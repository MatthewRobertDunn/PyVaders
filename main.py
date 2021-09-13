
from gamecontext import GameContext
from math import cos, pi, sin
from random import random

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
from panda3d.core import ConfigVariableString
import pymunk
from entities.dynamicentity import DynamicEntity
from entities.physicsentity import PhysicsEntity
from entities.tickingentity import TickingEntity


coord_system = ConfigVariableString("coordinate-system")
print(coord_system)
coord_system.setValue("yup-right")


class MyApp(ShowBase):
    def __init__(self):
        self.entities = []
        self.statics = []
        self.new_entities = []

        ShowBase.__init__(self)
        # render.setShaderAuto()
        base.setBackgroundColor(0, 0, 0)
        lens = OrthographicLens()
        lens.setFilmSize(80*0.8, 60*0.8)  # Or whatever is appropriate for your scene
        base.cam.node().setLens(lens)
        base.cam.setPos(0,0,0)
        self.render_node = render.attachNewNode("Entire Screen")
        self.accept('c',self.ShowCamPos)
        self.physics = pymunk.Space()      # Create a Space which contain the simulation
        self.physics.damping = 0.99
        self.physics.gravity = 0,-9.81      # Set its gravity
        self.squares()
        self.taskMgr.add(self.physics_task, "physics")
    
    def ShowCamPos(self):
#        position = environ.getPos()
        x=base.camera.getX()
        y=base.camera.getY()
        z=base.camera.getZ()
        print(str(x)+":"+str(y)+":"+str(z))

    def physics_task(self, task):
        dt = round(globalClock.getDt(),2)
        self.physics.step(dt)

        for entity in self.entities:
            entity.tick(dt)

        self.spawn_entities()
        return Task.cont

    def squares(self):
        #Provide game entities with functions for spawning entities into the world and loading assets.
        context = GameContext()
        context.loader = self.loader
        context.spawn_entity = self.spawn_entity

        entity = DynamicEntity(context)
        self.spawn_entity(entity)

        entity = PhysicsEntity(context,(1.4,-10))      
        self.spawn_entity(entity)


    #creates all queued entities
    def spawn_entities(self):
        while self.new_entities:
            self._spawn_entity(self.new_entities.pop())

    #queues an entity for creation
    def spawn_entity(self, entity):
        self.new_entities.append(entity)
    
    #Internal spawn entities, this is only called once all entities are ticked 
    # to avoid race conditions to do with entity creation order
    def _spawn_entity(self, entity):
        #Add entity to renderer if it has any render model
        if entity.render_model is not None:
            entity.render_model.reparent_to(self.render_node)

        #add entity to physics simulation if it has a physics body.
        if (entity.physics_body is not None):
            self.physics.add(entity.physics_body) # add to physics world
        
        if(entity.physics_components):
            for component in entity.physics_components:
                self.physics.add(component)
        
        #Include entity in game ticks if it supports receiving them.
        if isinstance(entity,TickingEntity):
            self.entities.append(entity)
        else:
            self.statics.append(entity)


app = MyApp()
app.run()
