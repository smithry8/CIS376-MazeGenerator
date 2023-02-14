# Created by Ryan and Ian O'Strander
import GameEngine.Scene
from GameEngine.Engine import engine
import Maze
from GameEngine.Scene import Scene
# Main Program
if __name__ == "__main__":
    s = Scene()
    engine.scenes.append(s)
    engine.currentScene = s
    maze = Maze.Maze(20)
    engine.spawn(maze)
    engine.loop()



