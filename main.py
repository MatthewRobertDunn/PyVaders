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
        
        self.rootNode = self.render.attachNewNode("rootNode")
        self.backgroundNode = self.rootNode.attachNewNode("backgroundRoot")
        self.gameNode = self.rootNode.attachNewNode("2dstuff")
        self.backgroundCamera = base.makeCamera(base.win,camName="camBack")
        self.backgroundCamera.reparentTo(self.backgroundNode)

        self.cardNode = self.loader.loadModel("gfx/scene.gltf")
        self.cardNode.setScale(0.01)
        self.cardNode.setPos(0, 0, -100)
        self.cardNode.reparentTo(self.backgroundNode)

        base.camera.reparentTo(self.gameNode)
        self.context.render_node.reparentTo(self.gameNode)
        self.backgroundCamera.node().setCameraMask(1)
        self.cam.node().setCameraMask(2)
        self.hideFromCamera(self.backgroundCamera, self.gameNode)
        self.hideFromCamera(self.cam, self.backgroundNode)

        #dlight = DirectionalLight('directionalLight')
        #dlight.setDirection(Vec3(0, 0, -2)) # (towards right-back-bottom; should only illuminate front/left/top )
        #dlight.setColor(Vec4(1, 1, 1, 1))
        #dlightNP = self.threeDNode.attachNewNode(dlight)
        #self.threeDNode.setLight(dlightNP)
        


    def hideFromCamera(self,camera1,nodePath):
        camera1Bits = BitArray()
        camera1Bits.setWord(0,camera1.node().getCameraMask().getWord())
        showMask =~(camera1Bits)
        hideMask = (camera1Bits)
        clearMask = BitArray.allOff()
        nodePath.node().adjustDrawMask(BitMask32(showMask.getWord(0).getWord()),hideMask.getWord(0).getWord(),clearMask.getWord(0).getWord())

    def physics_task(self, task):
        self.cardNode.setHpr(0,task.time,90)
        dt = round(globalClock.getDt(),4)
        self.keys.poll(base.mouseWatcherNode)
        self.context.tick(task.time,dt)
        return Task.cont

app = MyApp()
app.run()
