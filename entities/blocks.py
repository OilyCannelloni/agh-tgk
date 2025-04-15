import itertools
from random import random, randint

from entities.base import *
from grid.position import Position
from grid.grid import Grid

grid = Grid()


class WallSegment(Entity, ABC):
    THICKNESS = 10

    def __init__(self, start: Position, end: Position, color="white"):
        if start.x == end.x:
            height = abs(start.y - end.y)
            width = WallSegment.THICKNESS
            position = Position(start.x, min(start.y, end.y))
        elif start.y == end.y:
            height = WallSegment.THICKNESS
            width = abs(start.x - end.x)
            position = Position(start.y, min(start.x, end.x))
        else:
            raise NotImplementedError("Walls must be vertical or horizontal for now")

        super().__init__(position=position, width=width, height=height, color=color)


class ExampleInteractable(InteractableEntity, HackableEntity):
    def __init__(self, position: Position):
        self.color_cycle = itertools.cycle(("red", "green", "blue"))
        super().__init__(position=position, width=50, height=50, color=pygame.Color(next(self.color_cycle)))

    def set_color(self, color):
        self.sprite.image.fill(pygame.Color(color))

    def set_color_cycle(self, colors: tuple[str]):
        self.color_cycle = itertools.cycle(colors)

    @HackableMethod
    def on_player_interaction(self):
        # next(self.color_cycle) # try uncommenting me!
        color = next(self.color_cycle)
        self.set_color(color)


class WallBuilder(HackableEntity, ABC):
    def __init__(self, position: Position):
        super().__init__(position=position, width=20, height=20, color="pink")
        self.add_on_game_tick(self.build_wall, 50)
        self.display_hackable_methods()

    @HackableMethod
    def build_wall(self, **kwargs):
        if random() > 0.02:
            return

        start = Position(randint(300, 700), randint(300, 700))
        if random() < 0.5:
            end = Position(start.x, randint(300, 700))
        else:
            end = Position(randint(300, 700), start.y)

        grid.place_entity("WallSegment", start, end)

    @HackableMethod
    def nothing(self):
        print("adwsdads")

    def stuff(self):
        print("stuff")
