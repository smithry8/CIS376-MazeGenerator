# Created By Ian O'Strander
from GameEngine import GameObject


# Holds all of gameobjects
class Scene:
    #holds all gameobjects that are updateable
    updateable = []
    #holds all gameobjects that are updateable
    drawable = []
    #holds all gameobjects
    gameobjects = []
    #holds all gameobjects that have the function earlyUpdate
    earlyupdates = []
    #holds all gameobjects that have the function lateUpdate
    lateupdates = []
    # True if the Maze is no longer updating
    stable = False
    def __init__(self):
        pass
    # adds the gameobject in to the scene and puts them in the correct lists
    def spawn(self, gameobject):
        self.gameobjects.append(gameobject)
        t = type(gameobject)
        if hasattr(gameobject, "earlyUpdate"):
            self.earlyupdates.append(gameobject)
        if hasattr(gameobject, "lateUpdate"):
            self.lateupdates.append(gameobject)
        if issubclass(t, GameObject.DUGameObject):
            self.updateable.append(gameobject)
            self.drawable.append(gameobject)
        elif issubclass(t, GameObject.DGameObject):
            self.drawable.append(gameobject)
        elif issubclass(t, GameObject.UGameObject):
            self.updateable.append(gameobject)
    # removes gameobject from the scene
    def destroy(self, gameobject):
        self.gameobjects.remove(gameobject)
        t = type(gameobject)
        if hasattr(gameobject, "earlyUpdate"):
            self.earlyupdates.remove(gameobject)
        if hasattr(gameobject, "lateUpdate"):
            self.lateupdates.remove(gameobject)
        if issubclass(t, GameObject.DUGameObject):
            self.updateable.remove(gameobject)
            self.drawable.remove(gameobject)
        elif issubclass(t, GameObject.DGameObject):
            self.drawable.remove(gameobject)
        elif issubclass(t, GameObject.UGameObject):
            self.updateable.remove(gameobject)


