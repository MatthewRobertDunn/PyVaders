from engine.invader_context import InvaderContext
from keys import GameKeys
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
from panda3d.core import ConfigVariableString
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
        self.keys = GameKeys()
        base.setFrameRateMeter(True)
        #base.messenger.toggleVerbose()
        base.setBackgroundColor(0, 0, 0)
        lens = OrthographicLens()
        lens.setFilmSize(80*0.8, 60*0.8)  # Or whatever is appropriate for your scene
        base.cam.node().setLens(lens)
        base.cam.setPos(0,0,0)
        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(0, 0, -1)) # (towards right-back-bottom; should only illuminate front/left/top )
        dlight.setColor(Vec4(1, 1, 1, 1))
        dlightNP = render.attachNewNode(dlight)
        render.setLight(dlightNP)
        self.taskMgr.add(self.physics_task, "physics",None,None,-100)
        self.context = InvaderContext(self.keys, self.loader)
        self.context.render_node.reparentTo(self.render)

    def physics_task(self, task):
        dt = round(globalClock.getDt(),4)
        self.keys.poll(base.mouseWatcherNode)
        self.context.tick(task.time,dt)
        return Task.cont

app = MyApp()
app.run()
