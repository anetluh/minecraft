from direct.showbase.ShowBase import ShowBase
from map import Mapmanager
from hero import Hero
from direct.gui.OnscreenText import OnscreenText
class Game(ShowBase):
    def __init__(self):
        super().__init__()
        

        self.camera.setPos(0, 0, 0)
        self.camLens.setFov(100)
                                   

        self.land = Mapmanager()
        x,y,z = self.land.loadland("land.txt")
        self.hero = Hero((5,5,18.5), self.land)
        self.skybox()
    def skybox(self):
        self.sky = loader.loadModel('skybox/skybox.egg')
        self.sky.setScale(500)
        self.sky.setBin('background',1)
        self.sky.setLightOff()
        self.sky.reparentTo(render)




game = Game()
game.run()     
