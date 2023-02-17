from GameEngine import GameObject
from GameEngine.Engine import engine
import pygame
from Apple import Apple
class Snake(GameObject.DUGameObject):
    def __init__(self, player, color, x, y, w, h, layer, tag, collidable):
        super().__init__(x, y, w, h, layer, tag, collidable)
        self.player = player
        self.color = color
        self.speed = 30
        self.directions = {
            "up": [0,-1],
            "down": [0, 1],
            "left": [-1,0],
            "right": [1,0]
        }
        self.length = 3
        self.dir = [1,0]
        self.snake = [(self.x, self.y), (self.x, self.y+30), (self.x, self.y+60)]
        self.wrapping = False
    def Update(self):
        self.checkWrapping()
        for event in engine.keyboardInputs:
            if self.player == 1:
                if event.key == pygame.K_d and self.dir != self.directions["left"]:
                    self.dir = self.directions["right"]
                elif event.key == pygame.K_a and self.dir != self.directions["right"]:
                    self.dir = self.directions["left"]
                elif event.key == pygame.K_w and self.dir != self.directions["down"]:
                    self.dir = self.directions["up"]
                elif event.key == pygame.K_s and self.dir != self.directions["up"]:
                    self.dir = self.directions["down"]
            elif self.player == 2:
                if event.key == pygame.K_RIGHT and self.dir != self.directions["left"]:
                    self.dir = self.directions["right"]
                elif event.key == pygame.K_LEFT and self.dir != self.directions["right"]:
                    self.dir = self.directions["left"]
                elif event.key == pygame.K_UP and self.dir != self.directions["down"]:
                    self.dir = self.directions["up"]
                elif event.key == pygame.K_DOWN and self.dir != self.directions["up"]:
                    self.dir = self.directions["down"]
        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed
        self.snake.insert(0,(self.x,self.y))
        if len(self.snake) > self.length:
            self.snake.pop()
        if self.collisionDetector():
            engine._running = False

    def checkWrapping(self):
        screenWidth = engine._screen.get_width()
        screenHeight = engine._screen.get_height()
        tileSize = engine.tileSize
        offset = tileSize * 0.75
        if self.x == screenWidth:
            self.x = tileSize * -1
        elif self.y == screenHeight:
            self.y = 0
        elif self.x < 0:
            self.x = screenWidth
        elif self.y < 0:
            self.y = screenHeight
    def Draw(self):
        head = True
        for segment in self.snake:
            if head:
                pygame.draw.circle(engine._screen, (self.color[0], self.color[1] - 50, self.color[2]), (segment[0] + engine.tileSize/2, segment[1] + engine.tileSize/2), self.w/2)
                head = False
            else:
                pygame.draw.rect(engine._screen, self.color,(segment[0], segment[1], self.w, self.h))

    def collisionDetector(self):
        for i in range(1, len(self.snake)):
            if self.x == self.snake[i][0] and self.y == self.snake[i][1]:
                return True
        snakes = []
        apples = []
        for s in engine.currentScene.gameobjects:
            if isinstance(s, Snake) and s != self:
                snakes.append(s)
            if isinstance(s, Apple):
                apples.append(s)
        for snake in snakes:
            for s in snake.snake:
                if self.x == s[0] and self.y == s[1]:
                    return True
        for a in apples:
            if self.x == a.x and self.y == a.y:
                self.length += 1
                engine.destroy(a)
                engine.spawn(Apple())
        return False