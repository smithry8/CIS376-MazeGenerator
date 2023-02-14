#Created by Ian O'Strander
#A class that holds information about a Wall
stable = False
import GameObject
import pygame,sys
from Engine import engine

# Object that holds all the information for the walls of the maze
class Wall(GameObject.DUGameObject):
    updated = False
    def __init__(self, x, y, w, h, row, col, color, maze, layer = 0, tag = "", collidable = False):
        GameObject.DUGameObject.__init__(self, x, y, w, h, layer, tag, collidable)
        # the row of the maze
        self.row = row
        # the column of the maze
        self.col = col
        self.alive = False
        self.color = color
        # reference to the maze the wall is in
        self.maze = maze

        # maze information
        self.gridSize = maze.gridSize
        self.gridBuffer = maze.gridBuffer
        self.tileSize = maze.tileSize
    # Updates the wall to either alive or dead
    def Update(self):
        # Checks to see if the Maze is in a stable state
        # If it is we don't want to update the walls
        if not self.maze.stable:
            self.updated = False
            neighbors = self.checkNeighbors()
            if self.alive and (neighbors < 1 or neighbors > 4):
                self.maze.gridBuffer[self.row][self.col] = False
                self.updated = True
            if not self.maze.grid[self.row][self.col].alive and neighbors == 3:
                self.maze.gridBuffer[self.row][self.col] = True
                self.updated = True
    # sets the color of the wall
    # sets whether the wall should be collidable
    # draws the walls
    def Draw(self):
        color = (0, 0, 0) if not self.alive else self.color
        self.collidable = True if self.alive else False
        pygame.draw.rect(engine._screen, color, (self.row * self.tileSize, self.col * self.tileSize, self.tileSize, self.tileSize))
    # checks all neighbors of a cell and returns the number of neighbors
    def checkNeighbors(self):
        neighbors = 0;
        for r in [self.row, self.row + 1, self.row - 1]:
            for c in [self.col, self.col + 1, self.col - 1]:
                if not (r < 0 or r >= self.gridSize or c < 0 or c >= self.gridSize) and (r, c) != (self.row, self.col):
                    if self.maze.grid[r][c].alive:
                        neighbors += 1
        return neighbors


