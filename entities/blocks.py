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
            self.height = abs(start.y - end.y)
            self.width = WallSegment.THICKNESS
            self.position = Position(start.x, min(start.y, end.y))
        elif start.y == end.y:
            self.height = WallSegment.THICKNESS
            self.width = abs(start.x - end.x)
            self.position = Position(start.y, min(start.x, end.x))
        else:
            raise NotImplementedError("Walls must be vertical or horizontal for now")

        main_hb = MainHitbox(owner=self, x=self.position.x, y=self.position.y, width=self.width, height=self.height)
        super().__init__(position=start, main_hitbox=main_hb)

        self.sprite = BaseSprite(
            pygame.Surface([self.width, self.height]),
            pygame.Rect(self.position.x, self.position.y, self.width, self.height))
        self.sprite.image.fill(pygame.color.Color(color))


class ExampleInteractable(InteractableEntity, HackableEntity):
    def __init__(self, position: Position):
        main_hb = MainHitbox(owner=self, x=position.x, y=position.y, width=50, height=50)
        super().__init__(position=position, main_hitbox=main_hb)

        self.color_cycle = itertools.cycle(("red", "green", "blue"))
        self.sprite = BaseSprite(
            pygame.Surface([50, 50]),
            pygame.Rect(position.x, position.y, 50, 50)
        )
        self.sprite.image.fill(pygame.Color(next(self.color_cycle)))

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
        super().__init__()
        self.sprite = BaseSprite(pygame.Surface([20, 20]), pygame.Rect(position.x, position.y, 20, 20))
        self.sprite.image.fill(pygame.color.Color("pink"))
        self.add_on_game_tick(self.build_wall, 50)
        self.display_hackable_methods()

    @HackableMethod
    def build_wall(self, *args, **kwargs):
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

