# Created by Ryan and Ian O'Strander
import pygame, sys
import Player
import Wall
import random
import copy
from pygame.locals import *
from tkinter import *
from tkinter import messagebox
import tkinter as tk

DISPLAYSURF = pygame.display.set_mode((600, 600))
gridSize = 20
tileSize = DISPLAYSURF.get_width() / gridSize
grid = [[0] * gridSize for i in range(gridSize)]
FRAME_RATE = 60
clock = pygame.time.Clock()
playerRadius = tileSize/2
player = Player.Player(playerRadius, playerRadius)
walls = []
stable = False

# The game Engine
class Engine:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Ryan and Ian Maze Generator / Solver')
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
                #Handle the Movement of the player
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if collisionDetector(player.x + tileSize, player.y)[1] == False:
                            player.x += tileSize
                            player.position = (player.x,player.y)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if collisionDetector(player.x - tileSize, player.y)[1] == False:
                            player.x -= tileSize
                            player.position = (player.x,player.y)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if collisionDetector(player.x, player.y - tileSize)[1] == False:
                            player.y -= tileSize
                            player.position = (player.x,player.y)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if collisionDetector(player.x, player.y + tileSize)[1] == False:
                            player.y += tileSize
                            player.position = (player.x,player.y)
                    # used to check if the player has reached the bottom right tile for win
                    if (player.x >= (gridSize - 1) * tileSize) and (player.y >= (gridSize - 1) * tileSize):
                        winGame()
                    if event.key == pygame.K_q:
                        quitGame()
                if event.type == pygame.MOUSEBUTTONUP:
                    print("THIS WORKED")
                    pos = pygame.mouse.get_pos()
                    result = collisionDetector(pos[0],pos[1])
                    if result[1] != False:
                        grid[result[0].row][result[0].col] = "X"
                        walls.remove(result[0])
            #calls one cycle every frame
            if(not stable):
                simCycle()
            render(self)
            #limits frame rate to the FRAME_RATE constant
            clock.tick(FRAME_RATE)

# Fills the board with either an X or W
# X is for dead cells
# W is for live cells
def initializeGame():
    # Initialize Maze with all Empty Spaces
    for i in range(gridSize):
        for j in range(gridSize):
            grid[i][j] = "X"
            print(grid[i][j], end=" ")
        print("\n")
    # Place initial Points on Maze
    for i in range(gridSize * 2):
        x = random.randint(0, gridSize - 1)
        y = random.randint(0, gridSize - 1)
        grid[x][y] = "W"
# Draw visible game objects
def render(self):
    self._screen.fill((1, 1, 1))
    drawWalls()
    drawLines()
    drawPlayer(player)
    pygame.display.flip()
# Draws a grid on the Maze
def drawLines():
    for i in range(gridSize):
        pygame.draw.line(DISPLAYSURF, (255, 255, 255), (i * tileSize, 0), (i * tileSize, DISPLAYSURF.get_height()))
    for j in range(gridSize):
        pygame.draw.line(DISPLAYSURF, (255, 255, 255), (0, j * tileSize), (DISPLAYSURF.get_width(), j * tileSize))
# Draws the Walls on the Maze
def drawWalls():
    for i in range(gridSize):
        for j in range(gridSize):
           if(grid[i][j] == "W"):
                pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (i * tileSize, j * tileSize, tileSize, tileSize))
# detects if a point collides with a Wall
def collisionDetector(x,y):
    for w in walls:
        if w.x < x < (w.x + tileSize) and y > w.y and y < (w.y + tileSize):
            return [w, True]
    return [None, False]

# one cycle of the simulation
def simCycle():
    print("CYCLE")
    global grid
    global stable
    updated = False
    gridCopy = copy.deepcopy(grid)
    for i in range(gridSize):
        for j in range(gridSize):
            neighbors = checkNeighbors(i,j)
            if grid[i][j] == "W" and (neighbors < 1 or neighbors > 4):
                gridCopy[i][j] = "X"
                updated = True
            if grid[i][j] == "X" and neighbors == 3:
                gridCopy[i][j] = "W"
                updated = True
    grid = gridCopy
    # Checks to see if the Maze is in a stable state
    # If it is we want to stop the simCycles and spawn the Wall objects
    if(not updated):
        stable = True
        spawnWalls()
# Loops through the grid and initializes a Wall object for every "W"
def spawnWalls():
    for i in range(gridSize):
        for j in range(gridSize):
            if grid[i][j] == "W":
                x = i * tileSize
                y = j * tileSize
                walls.append(Wall.Wall(i*tileSize, j*tileSize, tileSize, tileSize, (x + tileSize / 2, y + tileSize / 2), i, j))
# checks all neighbors of a cell and returns the number of neighbors
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

#pops up that you won and closes the application
def winGame():
    messagebox.showinfo("WINNER", "YOU WIN")
    pygame.quit()
    sys.exit()

def quitGame():
    ans = messagebox.askyesno("Quitting", "Are you sure you want to quit")
    if ans:
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    print("name:" + __name__)
    initializeGame()
    e = Engine()
    e.loop()



