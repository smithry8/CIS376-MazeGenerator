#Created By Ian O'Strander
import pygame, sys
from tkinter import messagebox

FRAME_RATE = 60
clock = pygame.time.Clock()
# The game Engine
class Engine:
    scene = None
    def __init__(self):
        # gets reference to the scene
        pygame.init()
        pygame.display.set_caption('Ryan and Ian Maze Generator / Solver')
        # game loop will run for as long as this is true
        self._running = False
        self._screen = pygame.display.set_mode((600, 600))
        self.keyboardInputs = []
        self.mouseInputs = None
    def loop(self):
        self._running = True
        while self._running:
            # EVENTS
            events = pygame.event.get()
            self.keyboardInputs = []
            self.mouseInputs = None
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.keyboardInputs.append(event)
                    if event.key == pygame.K_q:
                        self.quitGame()
                # Handles mouse touching walls
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouseInputs = pygame.mouse.get_pos()

            #calls one cycle every frame
            for updateables in self.scene.updateable:
                if hasattr(updateables, "earlyUpdate"):
                    updateables.earlyUpdate()
            # Update all of the walls
            for updateables in self.scene.updateable:
                updateables.Update()

            for updateables in self.scene.updateable:
                if hasattr(updateables, "lateUpdate"):
                    updateables.lateUpdate()
            engine._screen.fill((1, 1, 1))
            for drawables in self.scene.drawable:
                drawables.Draw()
            pygame.display.flip()
            #limits frame rate to the FRAME_RATE constant
            clock.tick(FRAME_RATE)

    # detects if a point collides with a rectangle
    # returns True if collided with an object and False if it doesn't
    # returns the object that it collides with
    def collisionDetector(self, x, y, gameobject = ""):
        for object in self.scene.gameobjects:
                if object.collidable and object.x < x < (object.x + object.w) and y > object.y and y < (object.y + object.h) and gameobject != object:
                    return [object, True]
        return [None, False]

    # Quit game dialog
    def quitGame(self):
        ans = messagebox.askyesno("Quitting", "Are you sure you want to quit")
        if ans:
            pygame.quit()
            sys.exit()
    def spawn(self, gameobject):
        if self.scene != None:
            self.scene.spawn(gameobject)
        else:
            print("SCENE NOT ADDED")

    def destroy(self, gameobject):
        if self.scene != None:
            self.scene.destroy(gameobject)
        else:
            print("SCENE NOT ADDED")


    # pops up that you won and closes the application
    def winGame(self):
        messagebox.showinfo("WINNER", "YOU WIN")
        pygame.quit()
        sys.exit()

engine = Engine()