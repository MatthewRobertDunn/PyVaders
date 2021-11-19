from engine.invader_context import InvaderContext
from keys import GameKeys
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
from panda3d.core import ConfigVariableString
from panda3d.core import DrawMask, BitArray
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
        self.keys = GameKeys()
        base.setFrameRateMeter(True)
        #base.messenger.toggleVerbose()
        base.setBackgroundColor(0, 0, 0)
        lens = OrthographicLens()
        lens.setFilmSize(16*5, 9*5)  # Or whatever is appropriate for your scene
        base.cam.node().setLens(lens)
        props = WindowProperties() 
        props.setSize(1600, 900) 
        base.win.requestProperties(props) 
        
        self.taskMgr.add(self.physics_task, "physics",None,None,-100)
        self.context = InvaderContext(self.keys, self.loader)
        
        self.background_node = self.render.attachNewNode("background_node")
        self.game_node = self.render.attachNewNode("game_node")
        self.hud_node = self.render.attachNewNode("hud_node")
        
        self.backgroundCamera = base.makeCamera(base.win,camName="camBack")
        self.backgroundCamera.reparentTo(self.background_node)
        lens = PerspectiveLens()
        lens.setFilmSize(16*5, 9*5)  # Or whatever is appropriate for your scene
        self.backgroundCamera.node().setLens(lens)


        base.camera.reparentTo(self.game_node)

        self.backgroundCamera.node().setCameraMask(1)
        self.cam.node().setCameraMask(2)
        self.hideFromCamera(self.backgroundCamera, self.game_node)
        self.hideFromCamera(self.cam, self.background_node)

        #dlight = DirectionalLight('directionalLight')
        #dlight.setDirection(Vec3(0, 0, -2)) # (towards right-back-bottom; should only illuminate front/left/top )
        #dlight.setColor(Vec4(1, 1, 1, 1))
        #dlightNP = self.game_node.attachNewNode(dlight)
        #self.game_node.setLight(dlightNP)

        self.context.game_node.reparentTo(self.game_node)
        self.context.background_node.reparentTo(self.background_node)
        self.context.hud_node.reparentTo(self.hud_node)


    def hideFromCamera(self,camera1,nodePath):
        camera1Bits = BitArray()
        camera1Bits.setWord(0,camera1.node().getCameraMask().getWord())
        showMask =~(camera1Bits)
        hideMask = (camera1Bits)
        clearMask = BitArray.allOff()
        nodePath.node().adjustDrawMask(BitMask32(showMask.getWord(0).getWord()),hideMask.getWord(0).getWord(),clearMask.getWord(0).getWord())

    def physics_task(self, task):
        dt = round(globalClock.getDt(),4)
        self.keys.poll(base.mouseWatcherNode)
        self.context.tick(task.time,dt)
        return Task.cont

app = MyApp()
app.run()
