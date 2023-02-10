# Created by Ian
import Updateable
import Drawable

# Object that holds all gameobject information
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

# Game object that is drawable
class DGameObject(GameObject,Drawable.Drawable):
    def __init__(self, x, y, w, h, layer, tag, collidable):
        GameObject.__init__(self, x, y, w, h, layer, tag, collidable)

# Game object that is updateable
class UGameObject(GameObject,Updateable.Updateable):
    def __init__(self, x, y, w, h, layer, tag, collidable):
        GameObject.__init__(self, x, y, w, h, layer, tag, collidable)

    def Update(self):
        pass

# Game object that is drawable and updateable
class DUGameObject(DGameObject, Updateable.Updateable):
    def __init__(self, x, y, w, h, layer, tag, collidable):
        DGameObject.__init__(self, x, y, w, h, layer, tag, collidable)