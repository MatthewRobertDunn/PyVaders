
import pymunk
from entities.dynamic_trait import DynamicTrait
from entities.missile import Missile
#A basic dynamic physics game entity
class PlayerEntity(DynamicTrait):

    #Create the physics component of the game entity.
    def create_physics_body(self, position):
        self.create_dynamic_rectangle_body(position, 4.0, 3.0)
        move_joint = pymunk.GrooveJoint(self.context.static_body, self.physics_body, (-100, position[1]), (100, position[1]), (0, 0))
        self.physics_components.append(move_joint)

    def create_graphics_model(self):
        #self.draw.create_card(5.0,5.0)  #Create a 5x5 card
        #self.draw.set_texture_from_file("gfx/player.png")
        self.draw.z_order = -4.0
        self.draw.set_model("gfx/ship/scene.gltf")
        self.draw.game_node.setHpr(0,-90,180)
        self.draw.game_node.flatten_light()
        #self.draw.create_debug_shape(self.physics_poly)

    #Main game logic
    def tick(self):
        if self.keys.right:
            self.physics_body.apply_force_at_local_point((500.0,0.0),(0,0))
            self.draw.game_node.setH(30)
        elif self.keys.left:
            self.physics_body.apply_force_at_local_point((-500.0,0.0),(0,0))
            self.draw.game_node.setH(-30)
        else:
            self.draw.game_node.setH(0)

        if self.keys.fire:
            self.at_most("fire_missile", self.fire_missile,0.25)    
        
    def fire_missile(self):
        missile = Missile(context = self.context,
                            position = (self.physics_body.position[0], self.physics_body.position[1]+2.5),
                            velocity=self.physics_body.velocity
                            )
        self.context.spawn_entity(missile)
