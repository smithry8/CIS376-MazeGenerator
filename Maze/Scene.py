# Created By Ian O'Strander
import pygame, sys
import Player
import Wall
import random
# Holds all of the gameobjects
class Scene:
    # all gameobjects that are updateable
    updateable = []
    DISPLAYSURF = pygame.display.set_mode((600, 600))
    # number of tiles per row and column
    gridSize = 20
    # size of each tile
    tileSize = DISPLAYSURF.get_width() / gridSize
    playerRadius = tileSize / 2
    player = Player.Player(playerRadius * 3, playerRadius * 3)
    # holds all of the squares
    grid = [[0] * 20 for i in range(20)]
    # used to prevent conflicting updates
    gridBuffer = [[0] * 20 for i in range(20)]
    # True if the Maze is not longer updating
    stable = False
    def __init__(self):
        self.initializeGame()

    # Fills the board with either an X or W
    # X is for dead cells
    # W is for live cells
    def initializeGame(self):
        # Initialize Maze with all Empty Spaces
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                self.grid[i][j] = Wall.Wall(i * self.tileSize, j * self.tileSize, i, j, False,
                                       (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),self)
                self.updateable.append(self.grid[i][j])
        # Place initial Points on Maze
        for i in range(self.gridSize * 2):
            x = random.randint(0, self.gridSize - 1)
            y = random.randint(0, self.gridSize - 1)
            self.grid[x][y].alive = True

    # Draws a grid on the Maze
    def drawLines(self):
        for i in range(self.gridSize):
            pygame.draw.line(self.DISPLAYSURF, (255, 255, 255), (i * self.tileSize, 0), (i * self.tileSize, self.DISPLAYSURF.get_height()))
        for j in range(self.gridSize):
            pygame.draw.line(self.DISPLAYSURF, (255, 255, 255), (0, j * self.tileSize), (self.DISPLAYSURF.get_width(), j * self.tileSize))

    # Draw visible game objects
    def render(self):
        self.DISPLAYSURF.fill((1, 1, 1))
        self.drawWalls()
        self.drawLines()
        self.drawPlayer(self.player)
        pygame.display.flip()

    # Draws the Walls on the Maze
    def drawWalls(self):
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                color = (0, 0, 0) if not self.grid[i][j].alive else self.grid[i][j].color
                pygame.draw.rect(self.DISPLAYSURF, color, (i * self.tileSize, j * self.tileSize, self.tileSize, self.tileSize))
    # Draws the player
    def drawPlayer(self,player):
        pygame.draw.circle(self.DISPLAYSURF, player.color, player.position, self.tileSize / 2)