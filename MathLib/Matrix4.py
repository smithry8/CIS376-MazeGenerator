import math
from MathLib import Vector3
class Matrix4:
    def __init__(self, v1,v2,v3,v4):
        self.v1 = Vector3.Vector3(v1[0],v1[1],v1[2],v1[3]);
        self.v2 = Vector3.Vector3(v2[0],v2[1],v2[2],v2[3]);
        self.v3 = Vector3.Vector3(v3[0],v3[1],v3[2],v3[3]);
        self.v4 = Vector3.Vector3(v4[0],v4[1],v4[2],v4[3]);
        self.matrix = [[v1[0],v2[0],v3[0],v4[0]],
                       [v1[1], v2[1], v3[1],v4[1]],
                       [v1[1], v2[1], v3[1],v4[1]],
                       [v1[2], v2[2], v3[2],v4[2]],
                        [v1[3], v2[3], v3[3],v4[3]]]
    def __add__(self, other):
        if len(self.matrix) != len(self.matrix) or len(self.matrix[0]) != len(self.matrix[0]):
            return;
        m = Matrix4((0,0,0,0),(0,0,0,0),(0,0,0,0), (0,0,0,0))
        for i in range(len(m.matrix) - 1):
            for j in range(len(m.matrix) - 1):
                m.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
        return m.matrix
    def __sub__(self, other):
        if len(self.matrix) != len(self.matrix) or len(self.matrix[0]) != len(self.matrix[0]):
            return;
        m = Matrix4((0,0,0,0),(0,0,0,0),(0,0,0,0), (0,0,0,0))
        for i in range(len(m.matrix) - 1):
            for j in range(len(m.matrix) - 1):
                m.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]
        return m.matrix
    def __mul__(self, other):
        if isinstance(other, Vector3.Vector3):
            x = other.dotProduct(self.v1)
            y = other.dotProduct(self.v2)
            z = other.dotProduct(self.v3)
            w = other.dotProduct(self.v4)
            return Vector3.Vector3(x,y,z,w)
        elif isinstance(other, Matrix4):
            m = Matrix4((0,0,0),(0,0,0),(0,0,0))
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        m[i][j] += self.matrix[i][k] * other.matrix[k][j]
            return m
        return None

    def __eq__(self, other):
        if not isinstance(other, Matrix4):
            return False
        return self.v1.__eq__(other.v1) and self.v2.__eq__(other.v2) and self.v2.__eq__(other.v2) and self.v2.__eq__(other.v2)