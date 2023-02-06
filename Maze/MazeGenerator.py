# Created by Ryan and Ian O'Strander
import pygame, sys
import Scene
import random
from tkinter import messagebox
import Engine

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
    s = Scene.Scene()
    e = Engine.Engine(s)
    e.loop()



