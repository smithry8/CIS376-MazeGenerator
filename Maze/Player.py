#Created by Ian O'Strander
# A class that holds information about the player
class Player:
    def __init__(self, x, y, color = (255,255,255)):
        self.position = (x,y)
        self.color = color
        self.x = x
        self.y = y