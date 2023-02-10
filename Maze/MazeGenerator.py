# Created by Ryan and Ian O'Strander
import Scene
from Engine import engine
import Player
import Maze
# Main Program
if __name__ == "__main__":
    s = Scene.Scene()
    engine.scenes.append(s)
    engine.currentScene = s
    maze = Maze.Maze(20)
    engine.spawn(maze)
    engine.loop()



