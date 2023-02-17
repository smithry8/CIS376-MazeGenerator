import Snake
import Map
from GameEngine.Engine import engine
from GameEngine import Scene
from Apple import Apple
import random
import GameEngine.Scene
if __name__ == "__main__":
    snake = Snake.Snake(1,(29, 155, 240),0,0,30,30,0,0,False)
    snake2 = Snake.Snake(2,(154, 50, 255), 90, 90, 30, 30, 0, 0, False)
    map = Map.Map((255,255,255),0,0,0,0,1,0,False)
    scene = Scene.Scene()
    engine.changeScreenSize(600,600)
    engine.backgroundColor = (24,24,24)
    engine.spawn(snake)
    engine.spawn(snake2)
    engine.spawn(Apple())
    engine.spawn(Apple())
    engine.spawn(Apple())
    engine.spawn(Apple())
    engine.spawn(Apple())
    engine.spawn(map)
    engine.FRAME_RATE = 10
    engine.loop()


