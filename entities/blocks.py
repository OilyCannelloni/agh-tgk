import itertools
from random import random, randint

from entities.base import *
from grid.position import Position
from grid.grid import Grid
from hacking.hackable_method import CallableMethod
from utils import tint_image

grid = Grid()


class WallSegment(Entity, ABC):
    THICKNESS = 10

    def __init__(self, start: Position, end: Position, color="white"):
        half = WallSegment.THICKNESS // 2
        if start.x == end.x:
            height = abs(start.y - end.y) + WallSegment.THICKNESS
            width = WallSegment.THICKNESS
            position = Position(start.x - half, min(start.y, end.y) - half)
        elif start.y == end.y:
            height = WallSegment.THICKNESS
            width = abs(start.x - end.x) + WallSegment.THICKNESS
            position = Position(min(start.x, end.x) - half, start.y - half)
        else:
            raise NotImplementedError("Walls must be vertical or horizontal for now")

        super().__init__(position=position, width=width, height=height, color=color)


class Button(InteractableEntity, ABC):
    def __init__(self, position: Position, **kwargs):
        super().__init__(position=position, width=30, height=30, color="orange", **kwargs)
        self.target = None
        self.release_tick = -1

    def set_target(self, entity: Entity):
        self.target = entity

    def click(self):
        if self.target is not None:
            try:
                self.target.trigger()
            except AttributeError:
                print(f"Can't trigger target: {self.target}")

    def on_player_interaction(self, tick_data):
        self.click()


class Trap(Entity, ABC):
    def __init__(self, position: Position, **kwargs):
        width = height = 30
        image = self._load_icon(width, height)
        super().__init__(position=position, width=width, height=height, color="red", custom_image=image, **kwargs)

    @staticmethod
    def _load_icon(width, height):
        try:
            image = pygame.image.load("resources/spider-web.png").convert_alpha()
        except pygame.error as e:
            raise RuntimeError(f"Failed to load teleporter image: {e}")
        image = pygame.transform.scale(image, (width, height))
        image = tint_image(image, "red")
        return image

    def on_collision_with(self, entity: "Entity"):
        entity.killed_by("Trap")