class Mapmanager():
    def __init__(self):
        self.grass_block = 'grass-block.glb'
        self.dirt_block  = "dirt-block.glb"
        self.stone_block = "stone-block.glb"
        self.startNew()
    
    def add_block(self,position,model):
        self.model = loader.loadModel(model)
        self.model.setPos(position)
        self.model.setScale(1,1,1)
        self.model.setHpr(0,90,0)
        self.model.reparentTo(render)
        
    def startNew(self):
        self.land = render.attachNewNode("Land")
        
    
    def clear(self):
        self.land.removeNode()
        self.startNew()
        
    def loadland(self,filename):
        self.clear()
        with open(filename) as f:
            y = 0
            for line in f:
                x = 0
                line = line.split(" ")
                for z in line:
                    for z0 in range(0,int(z)*2+2,2):
                        model = self.add_block((x,y,(z0+4)),self.select_block(int(z)*2+2,z0))
                    x+=2
                y +=2
        return x,y,int(z)
                            
                
    def select_block(self,z,z0):
        if z0 <= z//3:
            return self.stone_block
        elif  z0 > z-1:
            return self.dirt_block
        else:
            return self.grass_block 
        