from dataclasses import dataclass

@dataclass
class Vector:
    x: float
    y: float

    def scale(self, factor):
        return Vector(self.x * factor, self.y * factor)

    def add(self, vector: "Vector"):
        return Vector(self.x + vector.x, self.y + vector.y)


@dataclass
class Position:
    x: float
    y: float

    def add(self, vector: Vector):
        return Position(self.x + vector.x, self.y + vector.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"




RIGHT = Vector(1, 0)
UP = Vector(0, -1)
LEFT = Vector(-1, 0)
DOWN = Vector(0, 1)