
from math import cos, pi, sin
from random import random

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
from panda3d.core import ConfigVariableString
from dynamicentity import DynamicEntity
import pymunk

coord_system = ConfigVariableString("coordinate-system")
print(coord_system)
coord_system.setValue("yup-right")


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # render.setShaderAuto()
        base.setBackgroundColor(0, 0, 0)
        lens = OrthographicLens()
        lens.setFilmSize(80*0.8, 60*0.8)  # Or whatever is appropriate for your scene
        base.cam.node().setLens(lens)
        base.cam.setPos(0,0,0)
        self.accept('c',self.ShowCamPos)
        self.space = pymunk.Space()      # Create a Space which contain the simulation
        self.space.gravity = 0,-9.81      # Set its gravity
        self.squares()
        self.taskMgr.add(self.physics_task, "physics")
    
    def ShowCamPos(self):
#        position = environ.getPos()
        x=base.camera.getX()
        y=base.camera.getY()
        z=base.camera.getZ()
        print(str(x)+":"+str(y)+":"+str(z))

    def physics_task(self, task):
        dt = globalClock.getDt()
        self.space.step(dt)
        for entity in self.entities:
            entity.tick(dt)
        return Task.cont

    def squares(self):
        self.entities = []
        self.statics = []
        self.node = render.attachNewNode("Dummy Node Name")
        square = DynamicEntity(self.loader)
        self.spawn_entity(square)
        


    def spawn_entity(self, entity):
        if entity.model is not None:
            entity.model.reparent_to(self.node)                # add to renderer

        if (entity.body is not None) and (entity.poly is not None):
            self.space.add(entity.body, entity.poly) # add to physics world
        
        self.entities.append(entity)

app = MyApp()
app.run()
