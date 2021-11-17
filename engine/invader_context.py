from engine.physics_context import PhysicsContext
from entities.alienwave import AlienWave
from entities.playerentity import PlayerEntity
from entities.destructibleterrain import DestructibleTerrain

class InvaderContext(PhysicsContext):
    def __init__(self, keys, loader):
        super().__init__(keys, loader)
        self.create_world()

    def create_world(self):
        entity = AlienWave(context = self)
        self.spawn_entity(entity)

        entity = PlayerEntity(context = self,position = (0,-20))
        self.spawn_entity(entity)

        entity = DestructibleTerrain(context = self, position = (-20,-10))
        self.spawn_entity(entity)

        entity = DestructibleTerrain(context = self, position = (0,-10))
        self.spawn_entity(entity)

        entity = DestructibleTerrain(context = self, position = (20,-10))
        self.spawn_entity(entity)