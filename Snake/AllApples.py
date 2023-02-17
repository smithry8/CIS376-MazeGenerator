from GameEngine import GameObject
import pygame
import random
from Apple import Apple
from GameEngine.Engine import engine
class Apple(GameObject.GameObject):
    def __init__(self, x, y, w, h, layer, tag, collidable):
        super().__init__(x, y, w, h, layer, tag, collidable)
        self.apples = []
