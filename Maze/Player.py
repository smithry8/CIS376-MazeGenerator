#Created by Ian O'Strander
import Updateable
from Engine import engine
import pygame, sys
import GameObject
# A class that holds information about the player
class Player(GameObject.DUGameObject):
    def __init__(self, x, y, collidable, w = 0, h = 0, layer = 0, tag = "", color = (255,255,255)):
        GameObject.DUGameObject.__init__(self, x, y, w, h, layer, tag, collidable)
        self.position = (x, y)
        self.color = color
        self.radius = 15
        self.speed = 30

    def Update(self):
        self.checkWin()
        self.movePlayer()

    # Draws the player
    def Draw(self):
        pygame.draw.circle(engine._screen, self.color, self.position, self.radius)

    def checkWin(self):
        # used to check if the player has reached the bottom right tile for win
        if (self.x >= 540) and (self.y >= 540):
            engine.winGame()
    def movePlayer(self):
        for event in engine.keyboardInputs:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if not engine.collisionDetector(self.x + self.speed, self.y, self)[1] and \
                        self.x + self.speed < engine._screen.get_width():
                    self.x += self.speed
                    self.position = (self.x, self.y)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if not engine.collisionDetector(self.x - self.speed, self.y, self)[1] and \
                        self.x - self.speed >= 0:
                    self.x -= self.speed
                    self.position = (self.x, self.y)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if not engine.collisionDetector(self.x, self.y - self.speed, self)[1] and \
                        self.y - self.speed >= 0:
                    self.y -= self.speed
                    self.position = (self.x, self.y)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if not engine.collisionDetector(self.x, self.y + self.speed, self)[1] and \
                        self.y + self.speed < engine._screen.get_height():
                    self.y += self.speed
                    self.position = (self.x, self.y)
