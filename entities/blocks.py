from random import random, randint
from abc import ABC

import pygame

from entities.base import Entity, BaseSprite, DynamicEntity, GameTickAction, HackableEntity, HackableMethod
from grid.position import Position
from grid.grid import Grid
grid = Grid()


class WallSegment(Entity, ABC):
    THICKNESS = 10

    def __init__(self, start: Position, end: Position):
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


        hb = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        super().__init__(position=start, hitbox=hb)

        print(start, end, hb)


        self.sprite = BaseSprite(
            pygame.Surface([self.width, self.height]),
            pygame.Rect(self.position.x, self.position.y, self.width, self.height))
        self.sprite.image.fill(pygame.color.Color("white"))

    def is_passable_for(self, entity: "Entity"):
        return False

    def on_collision_with(self, entity: "Entity"):
        pass


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

        wall = WallSegment(start, end)
        grid.place_entity(wall)

    @HackableMethod
    def nothing(self):
        print("adwsdads")

    def stuff(self):
        print("stuff")

