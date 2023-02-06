#Created by Ian O'Strander
#A class that holds information about a Wall
stable = False
import Updateable
import copy

class Wall(Updateable.Updateable):
    updated = False
    def __init__(self,x,y,row,col,alive,color,scene):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.alive = alive
        self.color = color
        self.scene = scene
        self.gridSize = scene.gridSize
        self.gridBuffer = scene.gridBuffer
    # one cycle of the simulation
    def Update(self):
        # Checks to see if the Maze is in a stable state
        # If it is we don't want to update the walls
        if not self.scene.stable:
            self.updated = False
            neighbors = self.checkNeighbors()
            if self.alive and (neighbors < 1 or neighbors > 4):
                self.scene.gridBuffer[self.row][self.col] = False
                self.updated = True
                print("updated")
            if not self.scene.grid[self.row][self.col].alive and neighbors == 3:
                self.scene.gridBuffer[self.row][self.col] = True
                self.updated = True
                print("updated")

    # checks all neighbors of a cell and returns the number of neighbors
    def checkNeighbors(self):
        neighbors = 0;
        for r in [self.row, self.row + 1, self.row - 1]:
            for c in [self.col, self.col + 1, self.col - 1]:
                if not (r < 0 or r >= self.gridSize or c < 0 or c >= self.gridSize) and (r, c) != (self.row, self.col):
                    if self.scene.grid[r][c].alive:
                        neighbors += 1
        return neighbors


