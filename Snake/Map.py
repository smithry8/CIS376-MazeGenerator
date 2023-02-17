from GameEngine import GameObject
from GameEngine.Engine import engine
import pygame
class Map(GameObject.DGameObject):
    def __init__(self, color, x, y, w, h, layer, tag, collidable):
        super().__init__(x, y, w, h, layer, tag, collidable)
        self.color = color
    def Draw(self):
        for i in range(engine._screen.get_width()//engine.tileSize):
            pygame.draw.line(engine._screen, self.color , (i * engine.tileSize, 0), (i * engine.tileSize, engine._screen.get_height()))
        for j in range(engine._screen.get_width()//engine.tileSize):
            pygame.draw.line(engine._screen, self.color , (0, j * engine.tileSize), (engine._screen.get_width(), j * engine.tileSize))