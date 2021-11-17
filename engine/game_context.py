import pymunk
from entities.graphics_trait import GraphicsTrait
from entities.physics_trait import PhysicsTrait
from entities.ticking_trait import TickingTrait
from panda3d.core import NodePath

class GameContext:
    def __init__(self, keys, loader):
        self.entities = []
        self.statics = []
        self.created_entities = []  
        self.deleted_entities = []
        self.keys = keys
        self.loader = loader
        self.render_node = NodePath("GameContext")

    def tick(self, time, dt):
        TickingTrait.time = time #global time
        TickingTrait.delta_time = dt  #delta time
        self.despawn_entities()
        self.spawn_entities()
        for entity in self.entities:
            entity.tick()
            entity.update_graphics_model()


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

        if (isinstance(entity, PhysicsTrait)):
            self.physics.remove(entity.physics_body) # add to physics world
            self._remove_components(entity)

        if isinstance(entity,GraphicsTrait):
            entity.draw.render_model.removeNode()


    def _remove_components(self, entity):
        if(entity.physics_components is not None):
            for component in entity.physics_components:
                self.physics.remove(component)


    def _add_components(self, entity):
        if(entity.physics_components):
            for component in entity.physics_components:
                self.physics.add(component)
