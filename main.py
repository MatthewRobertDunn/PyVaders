
from keys import GameKeys
from entities.playerentity import PlayerEntity
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
coord_system.setValue("yup-right")

#Uncomment this to use dx
r = ConfigVariableString("load-display")
r.setValue("pandadx9")

#uncomment this to remove vsync
#s = ConfigVariableString("sync-video")
#s.setValue("false")

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.entities = []
        self.statics = []
        self.created_entities = []  
        self.deleted_entities = []
        self.keys = GameKeys()
        base.setFrameRateMeter(True)
        #base.messenger.toggleVerbose()
        # render.setShaderAuto()
        base.setBackgroundColor(0, 0, 0)
        lens = OrthographicLens()
        lens.setFilmSize(80*0.8, 60*0.8)  # Or whatever is appropriate for your scene
        base.cam.node().setLens(lens)
        base.cam.setPos(0,0,0)
        self.render_node = render.attachNewNode("Entire Screen")
        self.accept('c',self.ShowCamPos)
        self.physics = pymunk.Space()      # Create a Space which contain the simulation
        self.physics.damping = 0.2
        self.physics.gravity = 0,-9.81      # Set its gravity
        self.squares()
        self.taskMgr.add(self.physics_task, "physics",None,None,-100)
        h = self.physics.add_collision_handler(1, 1)
        h.separate = self.on_collision
    

    def on_collision(self, arbiter, space, data):
        entity1 = arbiter.shapes[0].entity
        entity2 = arbiter.shapes[1].entity
        entity1.on_collision(entity2)
        entity2.on_collision(entity1)

    def ShowCamPos(self):
#        position = environ.getPos()
        x=base.camera.getX()
        y=base.camera.getY()
        z=base.camera.getZ()
        print(str(x)+":"+str(y)+":"+str(z))

    def physics_task(self, task):
        dt = round(globalClock.getDt(),4)
        self.keys.poll(base.mouseWatcherNode)
        TickingEntity.time = task.time #global time
        TickingEntity.delta_time = dt  #delta time
        for entity in self.entities:
            entity.tick()
            entity.update_graphics_model()
        self.despawn_entities()
        self.spawn_entities()
        self.physics.step(dt)
        return Task.cont

    def squares(self):
        #Provide game entities with functions for spawning entities into the world and loading assets.
        context = GameContext()
        context.loader = self.loader
        context.spawn_entity = self.spawn_entity
        context.despawn_entity = self.despawn_entity
        context.static_body = self.physics.static_body #This is required for creating some joints.
        context.keys = self.keys

        #entity = DynamicEntity(context)
        #self.spawn_entity(entity)

        entity = PhysicsEntity(context,(1.4,-10))      
        self.spawn_entity(entity)

        entity = PlayerEntity(context,(0,-15))
        self.spawn_entity(entity)

    #creates all queued entities
    def spawn_entities(self):
        while self.created_entities:
            self._spawn_entity(self.created_entities.pop())

    #queues an entity for creation
    def spawn_entity(self, entity):
        self.created_entities.append(entity)
    
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


    def despawn_entities(self):
        while self.deleted_entities:
            self._despawn_entity(self.deleted_entities.pop())

    def despawn_entity(self, entity):
        self.deleted_entities.append(entity)

    def _despawn_entity(self, entity):
        if isinstance(entity,TickingEntity):
            self.entities.remove(entity)
        else:
            self.statics.remove(entity)

        if(entity.physics_components):
            for component in entity.physics_components:
                self.physics.remove(component)

        if (entity.physics_body is not None):
            self.physics.remove(entity.physics_body) # add to physics world

        if entity.render_model is not None:
            entity.render_model.removeNode()



app = MyApp()
app.run()
