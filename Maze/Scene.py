# Created By Ian O'Strander
import pygame, sys
import Player
import Wall
from Engine import engine
import GameObject
# Holds all of gameobjects
class Scene:
    # all gameobjects that are updateable
    updateable = []
    drawable = []
    gameobjects = []
    # True if the Maze is no longer updating
    stable = False
    def __init__(self):
        pass
    def spawn(self, gameobject):
        self.gameobjects.append(gameobject)
        t = type(gameobject)
        if issubclass(t, GameObject.DUGameObject):
            self.updateable.append(gameobject)
            self.drawable.append(gameobject)
        elif issubclass(t, GameObject.DGameObject):
            self.drawable.append(gameobject)
        elif issubclass(t, GameObject.UGameObject):
            self.updateable.append(gameobject)

    def destroy(self, gameobject):
        self.gameobjects.remove(gameobject)
        self.updateable.remove(gameobject)
        self.drawable.remove(gameobject)
        self.collidable.append(gameobject)


