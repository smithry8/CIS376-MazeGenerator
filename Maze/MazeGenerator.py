import pygame, sys
from Player import Player
import random
from pygame.locals import *

DISPLAYSURF = pygame.display.set_mode((600, 600))
gridSize = 20
tileSize = DISPLAYSURF.get_width() / gridSize
grid = [[0] * gridSize for i in range(gridSize)]
FRAME_RATE = 60
clock = pygame.time.Clock()
playerRadius = tileSize/2
player = Player(playerRadius, playerRadius)
class Engine:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Hello World')
        self._running = False
        self._screen = DISPLAYSURF
    def loop(self):
        self._running = True

        while self._running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.x += tileSize
                        player.position = (player.x,player.y)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.x -= tileSize
                        player.position = (player.x,player.y)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.y -= tileSize
                        player.position = (player.x,player.y)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        player.y += tileSize
                        player.position = (player.x,player.y)
            simCycle()
            render(self)
            clock.tick(FRAME_RATE)
def initializeGame():
    pygame.draw.circle(DISPLAYSURF, (0, 0, 255), (playerRadius, playerRadius), playerRadius)
    drawLines()
    for i in range(gridSize):
        for j in range(gridSize):
            grid[i][j] = "X"
            print(grid[i][j], end=" ")
        print("\n")
    for i in range(gridSize * 15):
        x = random.randint(0, gridSize - 1)
        y = random.randint(0, gridSize - 1)
        grid[x][y] = "W"
def render(self):
    self._screen.fill((1, 1, 1))
    drawLines()
    drawWalls()
    drawPlayer(player)
    pygame.display.flip()
def drawLines():
    for i in range(gridSize):
        pygame.draw.line(DISPLAYSURF, (255, 255, 255), (i * tileSize, 0), (i * tileSize, DISPLAYSURF.get_height()))
    for j in range(gridSize):
        pygame.draw.line(DISPLAYSURF, (255, 255, 255), (0, j * tileSize), (DISPLAYSURF.get_width(), j * tileSize))

def drawWalls():
    for i in range(gridSize):
        for j in range(gridSize):
            if(grid[i][j] == "W"):
                pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (i * tileSize, j * tileSize, tileSize, tileSize))

# one cycle of the simulation
def simCycle():
    for i in range(gridSize):
        for j in range(gridSize):
            neighbors = checkNeighbors(i,j)
            if neighbors < 1 or neighbors > 4:
                grid[i][j] = "D"
            if neighbors == 3:
                grid[i][j] = "B"
    for i in range(gridSize):
        for j in range(gridSize):
            if grid[i][j] == "D":
                grid[i][j] = "X"
            elif grid[i][j] == "B":
                grid[i][j] = "W"


def checkNeighbors(row,col):
    neighbors = 0;
    for r in [row, row + 1, row - 1]:
        for c in [col, col + 1, col -1]:
            if not(r < 0 or r >= gridSize or c < 0 or c >= gridSize) and (r,c) != (row,col):
                if grid[r][c] == "W":
                    neighbors += 1
    return neighbors

def drawPlayer(player):
    pygame.draw.circle(DISPLAYSURF, player.color, player.position, tileSize/2)


if __name__ == "__main__":
    print("name:" + __name__)
    initializeGame()
    e = Engine()
    e.loop()



