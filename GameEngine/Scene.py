# Created By Ian O'Strander
from GameEngine import GameObject
from GameEngine.Engine import engine
# Holds all of gameobjects
class Scene:
    def __init__(self):
        #add the scene to engines list of scenes
        engine.scenes.append(self)
        #make this scene the current scene
        engine.currentScene = self
        # holds all gameobjects that are updateable
        self.updateable = []
        # holds all gameobjects that are updateable
        self.drawable = []
        # holds all gameobjects
        self.gameobjects = []
        # holds all gameobjects that have the function earlyUpdate
        self.earlyupdates = []
        # holds all gameobjects that have the function lateUpdate
        self.lateupdates = []
        self.all_sprites = []
        self.camera = None
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
            self.layerInsert(gameobject)
        elif issubclass(t, GameObject.DGameObject):
            self.layerInsert(gameobject)
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
    def layerInsert(self, gameObject):
        for d in range(len(self.drawable)):
            if self.drawable[d].layer > gameObject.layer:
                self.drawable.insert(d, gameObject)
                return
        self.drawable.append(gameObject)


