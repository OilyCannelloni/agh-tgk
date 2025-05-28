import math
from dataclasses import dataclass

@dataclass
class I2D:
    x: float
    y: float


@dataclass
class Vector(I2D):
    def scale(self, factor):
        return Vector(self.x * factor, self.y * factor)

    def add(self, vector: "Vector"):
        return Vector(self.x + vector.x, self.y + vector.y)

    @staticmethod
    def from_angle(angle: float):
        return Vector(math.cos(angle), -math.sin(angle))

    def normalize(self):
        l = math.sqrt(self.x ** 2 + self.y ** 2)
        return Vector(self.x / l, self.y / l)


@dataclass
class Position(I2D):
    def __add__(self, vector: Vector):
        return Position(self.x + vector.x, self.y + vector.y)

    def rel_vector(self, other_pos: "Position"):
        return Position(other_pos.x - self.x, other_pos.y - self.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"




RIGHT = Vector(1, 0)
UP = Vector(0, -1)
LEFT = Vector(-1, 0)
DOWN = Vector(0, 1)