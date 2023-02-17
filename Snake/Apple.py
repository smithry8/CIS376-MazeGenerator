from GameEngine import GameObject
import pygame
import random
from GameEngine.Engine import engine
class Apple(GameObject.DGameObject):
    size = engine.tileSize

    def __init__(self, x = 0, y = 0, w = size, h = size, layer = 0, tag = "", collidable = False):
        super().__init__(x, y, w, h, layer, tag, collidable)
        self.x = random.randint(0, (engine._screen.get_width() // engine.tileSize)) * engine.tileSize
        self.y = random.randint(0, (engine._screen.get_width() // engine.tileSize)) * engine.tileSize
    def Draw(self):
        pygame.draw.rect(engine._screen, (255,0,0), (self.x, self.y, self.w, self.h))

