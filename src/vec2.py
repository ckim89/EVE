import math


class vec2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** (1 / 2.0)

    def __add__(self, a):
        return vec2(self.x + a.x, self.y + a.y)

    def __sub__(self, a):
        return vec2(self.x - a.x, self.y - a.y)

        def __mul__(self, a):
            return vec2(self.x * a, self.y * a)

        def __rmul__(self, a):
            return self.__mul__(self, a)

        def dot(self, a):
            return self.x * a.x + self.y * a.y

    def angle(self):
        if self.magnitude() == 0:
            return 0
        return math.degrees(math.atan2(self.y, self.x))
