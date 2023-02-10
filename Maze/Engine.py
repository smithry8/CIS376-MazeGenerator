#Created By Ian O'Strander and Ryan
import pygame, sys
from tkinter import messagebox

# Constant variable to set the frame rate
FRAME_RATE = 60
# Game clock
clock = pygame.time.Clock()
# The game Engine
class Engine:
    # holds the scene that is currently being displayed
    currentScene = None
    def __init__(self):
        # holds all of the scenes
        self.scenes = []
        # gets reference to the scene
        pygame.init()
        pygame.display.set_caption('Ryan and Ian Maze Generator / Solver')
        # game loop will run for as long as this is true
        self._running = False
        self._screen = pygame.display.set_mode((600, 600))
        #list that hold all of the keyboard events during a frame
        self.keyboardInputs = []
        #holds a mouse input
        self.mouseInputs = None
    def loop(self):
        self._running = True
        # Game Loop
        while self._running:
            # EVENTS
            events = pygame.event.get()

            # reset keyboard and mouse inputs
            self.keyboardInputs = []
            self.mouseInputs = None

            # loop through all of the events
            for event in events:
                # quits game
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                # processes keybord inputs
                if event.type == pygame.KEYDOWN:
                    self.keyboardInputs.append(event)
                    if event.key == pygame.K_q:
                        self.quitGame()
                # processes mouse inputs
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouseInputs = pygame.mouse.get_pos()

            # calls all objects with earlyUpdate function
            for updateables in self.currentScene.earlyupdates:
                if hasattr(updateables, "earlyUpdate"):
                    updateables.earlyUpdate()
            # calls every updateable objects Update function
            for updateables in self.currentScene.updateable:
                updateables.Update()
            # calls all objects with lateUpdate function
            for updateables in self.currentScene.lateupdates:
                if hasattr(updateables, "lateUpdate"):
                    updateables.lateUpdate()
            # clear screen
            engine._screen.fill((1, 1, 1))
            # draw all drawable objects
            for drawables in self.currentScene.drawable:
                drawables.Draw()
            pygame.display.flip()
            #limits frame rate to the FRAME_RATE constant
            clock.tick(FRAME_RATE)

    # detects if a point collides with a rectangle
    # returns True if collided with an object and False if it doesn't
    # returns the object that it collides with
    def collisionDetector(self, x, y, gameobject = None):
        for object in self.currentScene.gameobjects:
                if (object.collidable or gameobject == "mouse") and object.x < x < (object.x + object.w) and y > object.y and y < (object.y + object.h) and gameobject != object:
                    return [object, True]
        return [None, False]

    # Quit game dialog
    def quitGame(self):
        ans = messagebox.askyesno("Quitting", "Are you sure you want to quit")
        if ans:
            pygame.quit()
            sys.exit()

    #spawns gameobject in current scene
    def spawn(self, gameobject):
        if self.currentScene != None:
            self.currentScene.spawn(gameobject)
        else:
            print("SCENE NOT ADDED")
    #destroys gameobject in current scene
    def destroy(self, gameobject):
        if self.currentScene != None:
            self.currentScene.destroy(gameobject)
        else:
            print("SCENE NOT ADDED")


    # pops up that you won and closes the application
    def winGame(self):
        messagebox.showinfo("WINNER", "YOU WIN")
        pygame.quit()
        sys.exit()

engine = Engine()