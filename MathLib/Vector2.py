import math

class Vector2:
    def __init__(self, x, y, w=1):
        self.x = x
        self.y = y
        self.w = w
        self.vector = [x,y,w]

    def __repr__(self):
        return f"Vector2({self.x}, {self.y}, {self.w})"
    
    def crossProduct(self, other):
        z = self.x * other.y - self.y * other.x
        return Vector2(0, 0, z)
    
    def dotProduct(self, other):
        return self.x * other.x + self.y * other.y
    
    def angleBetween(self, other):
        dotProductVar = self.dotProduct(other)
        magnitudeProductVar = self.magnitude() * other.magnitude()
        return math.acos(dotProductVar / magnitudeProductVar)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def normalize(self):
        magnitude = self.magnitude()
        return Vector2(self.x / magnitude, self.y / magnitude)
    
    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return False