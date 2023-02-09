# Created by Ryan and Ian O'Strander
import Scene
from Engine import engine
import Player
import Maze
# Main Program
if __name__ == "__main__":
    s = Scene.Scene()
    engine.scene = s
    player = Player.Player(45, 45, 1, True)
    maze = Maze.Maze(20)
    engine.spawn(player)
    engine.spawn(maze)
    engine.loop()



