from direct.gui.OnscreenImage import OnscreenImage  # Імпорт класу для роботи з зображеннями на екрані
from panda3d.core import TransparencyAttrib  # Імпорт атрибута прозорості
from panda3d.core import WindowProperties  # Імпорт класу для налаштування вікна
from direct.showbase.ShowBase import ShowBase  # Імпорт базового класу для гри
from panda3d.core import CollisionTraverser, CollisionNode, CollisionRay, CollisionHandlerQueue  # Імпорт класів для обробки колізій
from direct.gui.OnscreenImage import OnscreenImage  # Імпорт класу для роботи з зображеннями на екрані
from panda3d.core import BitMask32  # Імпорт класу для бітових масок

key_switch_camera = 'c' 
key_switch_mode = 'z' 
key_forward = 'w'  
key_back = 's'      
key_left = 'a'      
key_right = 'd'     
key_up = 'e'      
key_down = 'q'    

key_turn_left = 'n' 
key_turn_right = 'm'
class Hero():
    def __init__(self, pos,land):
        self.land = land
        self.mode = True
        self.hero = loader.loadModel("steve.glb")
        self.hero.setScale(0.10)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.mouseLook = False
        self.hero.setHpr(0,90,0)
        self.cameraBind()
        self.accept_events()

        self.grass_block = 'grass-block.glb'
        self.dirt_block  = "dirt-block.glb"
        self.stone_block = "stone-block.glb"

        self.rayQueue = CollisionHandlerQueue()
        self.traverser = CollisionTraverser()

        ray = CollisionRay()
        ray.setOrigin(0, 0, 0)
        ray.setDirection(0, 1, 0)
        
        rayNode = CollisionNode("ray")
        rayNode.addSolid(ray)
        rayNode.setCollisionMask(BitMask32.bit(1))
        self.rayNodePath = base.camera.attachNewNode(rayNode)
        self.traverser.addCollider(self.rayNodePath, self.rayQueue)
        self.rayNodePath.show()
        self.mouseLookEnabled = True


    def mouseTask(self):
        if self.mouseLookEnabled and base.mouseWatcher.Node.hasMouse:
            mX = base.win.getPointer(0).getX()
            mY = base.win.getPointer(0).getY()   

            deltaX = (mX - base.win.getXSize()) // 2
            deltaY = (mX - base.win.getYSize()) // 2

            self.hero.setH(self.hero.getH() - deltaX*0.1)
            self.hero.setH(self.hero.getY() - deltaY*(-0.1))

            base.win.movePointer(0, base.win.getXSize()) // 2, base.win.getYSize()) // 2 )

        return task.cont
    




    def cameraBind(self):
        base.disableMouse()
        base.camera.setHpr(90,90,90)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(5,8,15)
        self.cameraOn = 1
        crosshair = OnscreenImage(
            image = "crosshairs.png",
            pos = (0,0,0),
            scale = 0.05,
            )
        crosshair.setTransparency(TransparencyAttrib.MAlpha)
        props = WindowProperties()
        props.setCursorHidden(1)
        props.setMouseMode(WindowProperties.M_confined)
        base.win.requestProperties(props)

    def cameraUP(self):
        base.enableMouse()
        base.camera.setPos(0,0,10)
        base.camera.reparentTo(render)
        props = WindowProperties()
        props.setCursorHidden(0)
        props.setMouseMode(WindowProperties.M_absolute)
        base.win.requestProperties(props)
        self.cameraOn = 0






    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()
    def turn_left(self):
            self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def look_at(self, angle):

        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
    
    def check_dir(self,angle):

        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)


    def forward(self):
        angle =(self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH()+180) % 360
        self.move_to(angle)
    
    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)
    def changeMode(self):
       if self.mode:
           self.mode = False
       else:
           self.mode = True
           

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)


    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)

        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.changeMode)


        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)















