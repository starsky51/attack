# general utility functions/classes

from math import *

class Vector2D:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def direction(self):
        return degrees(atan(self.y / self.x))

    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2)