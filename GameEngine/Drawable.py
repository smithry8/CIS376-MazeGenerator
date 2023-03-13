# Created by Ian # Created by Ian
from abc import ABC, abstractmethod
import pygame as pg
# Interface for drawable objects
class Drawable(ABC):
    @abstractmethod
    def Draw(self):
        pass