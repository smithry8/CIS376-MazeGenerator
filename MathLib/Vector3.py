import math

class Vector3:
    def __init__(self, x, y, z, w=1):
        self.x = x
        self.y = y
        self.w = w
        self.z = z
        self.vector = [x,y,w,z]

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z}, {self.w})"
    
    def crossProduct(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector3(x, y, z)
    
    def dotProduct(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def angleBetween(self, other):
        dotProductVar = self.dotProduct(other)
        magnitudeProductVar = self.magnitude() * other.magnitude()
        print(dotProductVar , "/" , magnitudeProductVar)
        return math.acos(dotProductVar / magnitudeProductVar)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def normalize(self):
        magnitude = self.magnitude()
        return Vector3(self.x / magnitude, self.y / magnitude, self.z / magnitude)
    
    def __eq__(self, other):
        if isinstance(other, Vector3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False