import pygame, sys
import Player
import Wall
import random
class Scene:
    updateable = []
    DISPLAYSURF = pygame.display.set_mode((600, 600))
    gridSize = 20
    tileSize = DISPLAYSURF.get_width() / gridSize
    playerRadius = tileSize / 2
    player = Player.Player(playerRadius * 3, playerRadius * 3)
    grid = [[0] * 20 for i in range(20)]
    gridBuffer = [[0] * 20 for i in range(20)]
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

    def drawPlayer(self,player):
        pygame.draw.circle(self.DISPLAYSURF, player.color, player.position, self.tileSize / 2)