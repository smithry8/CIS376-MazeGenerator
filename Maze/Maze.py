import GameObject
from Engine import engine
import pygame
import random
import Wall
import Player
class Maze(GameObject.DUGameObject):
    def __init__(self, gridSize, x=-1, y=-1, w=-1, h= -1, layer = -1, tag="", collidable=False):
        GameObject.DUGameObject.__init__(self, x, y, w, h, layer, tag, collidable)
        # number of tiles per row and column
        self.gridSize = gridSize
        # size of each tile
        self.tileSize = engine._screen.get_width() / gridSize
        # holds all the squares
        self.grid = [[0] * gridSize for i in range(gridSize)]
        # used to prevent conflicting updates
        self.gridBuffer = [[0] * gridSize for i in range(gridSize)]
        self.initializeGame()
        # True if the walls are no longer updating
        self.stable = False

    #Gets called before Update
    def earlyUpdate(self):
        if not self.stable:
            for i in range(self.gridSize):
                for j in range(self.gridSize):
                    self.gridBuffer[i][j] = self.grid[i][j].alive
    def Update(self):
        pass
    # draws the lines on the maze
    def Draw(self):
        for i in range(self.gridSize):
            pygame.draw.line(engine._screen, (255, 255, 255), (i * self.tileSize, 0),
                             (i * self.tileSize, engine._screen.get_height()))
        for j in range(self.gridSize):
            pygame.draw.line(engine._screen, (255, 255, 255), (0, j * self.tileSize),
                             (engine._screen.get_width(), j * self.tileSize))

    #Gets called after Update
    def lateUpdate(self):
        # updates grid with the new walls, also checks to see if the maze is stable
        if not self.stable:
            isStable = True
            for i in range(self.gridSize):
                for j in range(self.gridSize):
                    self.grid[i][j].alive = self.gridBuffer[i][j]
                    if not self.stable:
                        if self.grid[i][j].updated == True:
                            isStable = False
            if isStable:
                self.stable = True
                player = Player.Player(45, 45, 1, True)
                engine.spawn(player)
        # gets mouse inputs and stores them in pos
        pos = engine.mouseInputs
        # if there is mouse inputs check to see if it collids with a wall
        if pos != None:
            result = engine.collisionDetector(pos[0], pos[1], "mouse")
            if result[1] == True:
                # flip wall alive state
                self.grid[result[0].row][result[0].col].alive = not self.grid[result[0].row][result[0].col].alive

    # Fills the board with either an X or W
    # X is for dead cells
    # W is for live cells
    def initializeGame(self):
        # Initialize Maze with all Empty Spaces
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                self.grid[i][j] = Wall.Wall(i * self.tileSize, j * self.tileSize, self.tileSize, self.tileSize, i, j, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),self)
                engine.spawn(self.grid[i][j])

        # Place initial Points on Maze
        for i in range(self.gridSize * 2):
            x = random.randint(0, self.gridSize - 1)
            y = random.randint(0, self.gridSize - 1)
            self.grid[x][y].alive = True


