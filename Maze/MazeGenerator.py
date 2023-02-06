# Created by Ryan and Ian O'Strander
import Scene
import Engine
# Main Program
if __name__ == "__main__":
    print("name:" + __name__)
    s = Scene.Scene()
    e = Engine.Engine(s)
    e.loop()



