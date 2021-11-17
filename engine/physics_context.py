import pymunk
from engine.game_context import GameContext

class PhysicsContext(GameContext):
    def __init__(self, keys, loader):
        super().__init__(keys,loader)
        self.physics_replace_entities = []
        self.physics = pymunk.Space()      # Create a Space which contain the simulation
        self.physics.damping = 0.2
        self.physics.gravity = 0,-9.81      # Set its gravity
        self.static_body = self.physics.static_body #This is required for creating some joints.
        h = self.physics.add_collision_handler(1, 1)
        h.post_solve = self.on_collision

    def tick(self, time, dt):
        self.replace_physics()
        super().tick(time,dt)
        self.physics.step(dt)

    def on_collision(self, arbiter, space, data):
        entity1 = arbiter.shapes[0].entity
        entity2 = arbiter.shapes[1].entity
        if entity1.is_alive and entity2.is_alive:
            contact1 = arbiter.contact_point_set.points[0].point_a
            contact2 = arbiter.contact_point_set.points[0].point_b
            entity1.on_collision(entity2, contact1, contact2)
            entity2.on_collision(entity1, contact2, contact1)

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
