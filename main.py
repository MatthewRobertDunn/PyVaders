
from entities.alien import Alien
from entities.destructibleterrain import DestructibleTerrain
from entities.graphics_trait import GraphicsTrait
from entities.physics_trait import PhysicsTrait
from entities.ticking_trait import TickingTrait
from engine.graphic import Graphic
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
from entities.alienwave import AlienWave

coord_system = ConfigVariableString("coordinate-system")
coord_system.setValue("yup-right")

#Uncomment this to use dx
#r = ConfigVariableString("load-display")
#r.setValue("pandadx9")

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
        self.physics_replace_entities = []
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
        self.taskMgr.add(self.physics_task, "physics",None,None,-100)
        h = self.physics.add_collision_handler(1, 1)
        h.post_solve = self.on_collision
        self.create_world()

    def on_collision(self, arbiter, space, data):
        entity1 = arbiter.shapes[0].entity
        entity2 = arbiter.shapes[1].entity
        if entity1.is_alive and entity2.is_alive:
            contact1 = arbiter.contact_point_set.points[0].point_a
            contact2 = arbiter.contact_point_set.points[0].point_b
            entity1.on_collision(entity2, contact1, contact2)
            entity2.on_collision(entity1, contact2, contact1)

    def ShowCamPos(self):
#        position = environ.getPos()
        x=base.camera.getX()
        y=base.camera.getY()
        z=base.camera.getZ()
        print(str(x)+":"+str(y)+":"+str(z))

    def physics_task(self, task):
        dt = round(globalClock.getDt(),4)
        self.keys.poll(base.mouseWatcherNode)
        TickingTrait.time = task.time #global time
        TickingTrait.delta_time = dt  #delta time
        for entity in self.entities:
            entity.tick()
            entity.update_graphics_model()
        self.despawn_entities()
        self.replace_physics()
        self.spawn_entities()
        self.physics.step(dt)
        return Task.cont

    def create_world(self):
        #Provide game entities with functions for spawning entities into the world and loading assets.
        context = GameContext()
        context.loader = self.loader
        context.spawn_entity = self.spawn_entity
        context.despawn_entity = self.despawn_entity
        context.static_body = self.physics.static_body #This is required for creating some joints.
        context.replace_physics_components = self.replace_physics_components
        context.keys = self.keys

        entity = AlienWave(context = context)
        self.spawn_entity(entity)

        entity = PlayerEntity(context = context,position = (0,-20))
        self.spawn_entity(entity)

        entity = DestructibleTerrain(context = context, position = (0,0))
        self.spawn_entity(entity)

        alien = Alien(context=context, position=(0,-10))
        self.spawn_entity(alien)
        

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
        if isinstance(entity,GraphicsTrait):
            entity.draw.render_model.reparent_to(self.render_node)

        #add entity to physics simulation if it has a physics body.
        if (isinstance(entity, PhysicsTrait)):
            self.physics.add(entity.physics_body) # add to physics world
            #Add physics components.
            self._add_components(entity)        

        #Include entity in game ticks if it supports receiving them.
        if isinstance(entity,TickingTrait):
            self.entities.append(entity)
        else:
            self.statics.append(entity)
        entity.is_alive = True
        entity.on_spawn()


    def replace_physics_components(self, entity, new_components):
        self.physics_replace_entities.append((entity,new_components))

    def replace_physics(self):
        while self.physics_replace_entities:
            self._replace_physics(*self.physics_replace_entities.pop())

    def _replace_physics(self, entity, new_components):
        #Remove old components
        self._remove_components(entity)
        entity.physics_components = new_components
        self._add_components(entity)



    def despawn_entities(self):
        while self.deleted_entities:
            self._despawn_entity(self.deleted_entities.pop())

    def despawn_entity(self, entity):
        if entity.is_alive == False:
            return
        else:
            entity.is_alive = False
            self.deleted_entities.append(entity)

    def _despawn_entity(self, entity):
        if isinstance(entity,TickingTrait):
            self.entities.remove(entity)
        else:
            self.statics.remove(entity)

        if (entity.physics_body is not None):
            self.physics.remove(entity.physics_body) # add to physics world

        self._remove_components(entity)

        if isinstance(self, Graphic) is not None:
            entity.draw.render_model.removeNode()


    def _remove_components(self, entity):
        if(entity.physics_components is not None):
            for component in entity.physics_components:
                self.physics.remove(component)


    def _add_components(self, entity):
        if(entity.physics_components):
            for component in entity.physics_components:
                self.physics.add(component)

app = MyApp()
app.run()
