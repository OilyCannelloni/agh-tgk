from abc import ABC, abstractmethod

from entities.blocks import WallSegment
from grid.grid import Grid
from grid.position import Position, Vector
from terminal.terminal import Terminal

grid = Grid()


class Level(ABC):
    _active_level = None

    @classmethod
    @abstractmethod
    def load(cls):
        grid.clear()
        if Terminal.initialized:
            Terminal().clear()
        Level._active_level = cls

    @staticmethod
    def load_last():
        Level._active_level.load()

    @staticmethod
    def make_wall_cell(cell_type: str, cell_size: int, center: Position):
        half = cell_size // 2
        if "n" in cell_type:
            WallSegment(center + Vector(-half, -half), center + Vector(half, -half))
        if "e" in cell_type:
            WallSegment(center + Vector(half, -half), center + Vector(half, half))
        if "s" in cell_type:
            WallSegment(center + Vector(-half, half), center + Vector(half, half))
        if "w" in cell_type:
            WallSegment(center + Vector(-half, -half), center + Vector(-half, half))
