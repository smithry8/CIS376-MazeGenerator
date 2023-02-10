import Updateable
import Drawable
class GameObject():
    def __init__(self,x,y,w,h,layer,tag,collidable):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.y = y
        self.tag = tag
        self.layer = layer
        self.collidable = collidable
class DGameObject(GameObject,Drawable.Drawable):
    def __init__(self, x, y, w, h, layer, tag, collidable):
        GameObject.__init__(self, x, y, w, h, layer, tag, collidable)
class UGameObject(GameObject,Updateable.Updateable):
    def __init__(self, x, y, w, h, layer, tag, collidable):
        GameObject.__init__(self, x, y, w, h, layer, tag, collidable)

    def Update(self):
        pass
class DUGameObject(DGameObject, Updateable.Updateable):
    def __init__(self, x, y, w, h, layer, tag, collidable):
        DGameObject.__init__(self, x, y, w, h, layer, tag, collidable)