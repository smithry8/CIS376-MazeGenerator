#Created By Ian O'Strander
import pygame, sys
from tkinter import messagebox

FRAME_RATE = 60
clock = pygame.time.Clock()
# The game Engine
class Engine:
    def __init__(self, scene):
        # gets reference to the scene
        self.scene = scene
        pygame.init()
        pygame.display.set_caption('Ryan and Ian Maze Generator / Solver')
        # game loop will run for as long as this is true
        self._running = False
        # initialize screen
        self._screen = scene.DISPLAYSURF
    def loop(self):
        self._running = True
        while self._running:
            # used to check if the player has reached the bottom right tile for win
            if (self.scene.player.x >= (self.scene.gridSize - 2) * self.scene.tileSize) and (self.scene.player.y >= (self.scene.gridSize - 2) * self.scene.tileSize):
                self.winGame()
            # EVENTS
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                #Handle the Movement of the player
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.collisionDetector(self.scene.player.x + self.scene.tileSize, self.scene.player.y)[1] == False and self.scene.player.x + self.scene.tileSize < self.scene.DISPLAYSURF.get_width():
                            self.scene.player.x += self.scene.tileSize
                            self.scene.player.position = (self.scene.player.x,self.scene.player.y)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.collisionDetector(self.scene.player.x - self.scene.tileSize, self.scene.player.y)[1] == False and self.scene.player.x - self.scene.tileSize >= 0:
                            self.scene.player.x -= self.scene.tileSize
                            self.scene.player.position = (self.scene.player.x,self.scene.player.y)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.collisionDetector(self.scene.player.x, self.scene.player.y - self.scene.tileSize)[1] == False and self.scene.player.y - self.scene.tileSize >= 0:
                            self.scene.player.y -= self.scene.tileSize
                            self.scene.player.position = (self.scene.player.x,self.scene.player.y)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if self.collisionDetector(self.scene.player.x, self.scene.player.y + self.scene.tileSize)[1] == False and self.scene.player.y + self.scene.tileSize < self.scene.DISPLAYSURF.get_height():
                            self.scene.player.y += self.scene.tileSize
                            self.scene.player.position = (self.scene.player.x,self.scene.player.y)
                    if event.key == pygame.K_q:
                        self.quitGame()
                # Handles mouse touching walls
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    result = self.collisionDetector(pos[0],pos[1])
                    self.scene.grid[result[0].row][result[0].col].alive = not self.scene.grid[result[0].row][result[0].col].alive
            #calls one cycle every frame
            # initiale the buffer with the current Maze
            for i in range(self.scene.gridSize):
                for j in range(self.scene.gridSize):
                    self.scene.gridBuffer[i][j] = self.scene.grid[i][j].alive
            # Update all of the walls
            for updateables in self.scene.updateable:
                updateables.Update()
            # Set our grid equal to the gridBuffer
            # Check to see if our grid is in a stable state, if so we should stop updating the walls
            isStable = True
            for i in range(self.scene.gridSize):
                for j in range(self.scene.gridSize):
                    self.scene.grid[i][j].alive = self.scene.gridBuffer[i][j]
                    if not self.scene.stable:
                        if self.scene.grid[i][j].updated == True:
                            isStable = False
            self.scene.stable = isStable
            # Have scene render its visible gameobjects
            self.scene.render()
            #limits frame rate to the FRAME_RATE constant
            clock.tick(FRAME_RATE)
    # detects if a point collides with a rectangle
    # return the wall that it collides with and True if it was a wall and false if it was a dead cell
    def collisionDetector(self, x,y):
        for i in range(self.scene.gridSize):
            for j in range(self.scene.gridSize):
                w = self.scene.grid[i][j]
                if w.x < x < (w.x + self.scene.tileSize) and y > w.y and y < (w.y + self.scene.tileSize):
                    return [w, True] if w.alive else [w,False]
        return [None, False]

    # Quit game dialog
    def quitGame(self):
        ans = messagebox.askyesno("Quitting", "Are you sure you want to quit")
        if ans:
            pygame.quit()
            sys.exit()

    # pops up that you won and closes the application
    def winGame(self):
        messagebox.showinfo("WINNER", "YOU WIN")
        pygame.quit()
        sys.exit()