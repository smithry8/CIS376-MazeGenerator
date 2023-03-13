# Created by Ian
from GameEngine import Updateable
from GameEngine import Drawable
import pygame as pg
# Object that holds all gameobject information
class GameObject():
    def __init__(self,x,y,w,h,tag,collidable):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.y = y
        self.tag = tag
        self.collidable = collidable

# Game object that is drawable
class DGameObject(GameObject, Drawable.Drawable, pg.sprite.Sprite):

    def __init__(self, x, y, w, h, tag, collidable):
        GameObject.__init__(self, x, y, w, h, tag, collidable)
        pg.sprite.Sprite.__init__(self)
        self.layer = 0

# Game object that is updateable
class UGameObject(GameObject,Updateable.Updateable):
    def __init__(self, x, y, w, h, tag, collidable):
        GameObject.__init__(self, x, y, w, h, tag, collidable)

    def Update(self):
        pass

# Game object that is drawable and updateable
class DUGameObject(DGameObject, Updateable.Updateable):
    def __init__(self, x, y, w, h, tag, collidable):
        DGameObject.__init__(self, x, y, w, h, tag, collidable)