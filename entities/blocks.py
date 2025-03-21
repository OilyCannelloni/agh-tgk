from abc import ABC

import pygame

from entities.base import Entity, BaseSprite
from grid.position import Position


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
        print(hb)


        self.sprite = BaseSprite(
            pygame.Surface([self.width, self.height]),
            pygame.Rect(self.position.x, self.position.y, self.width, self.height))
        self.sprite.image.fill(pygame.color.Color("white"))

    def is_passable_for(self, entity: "Entity"):
        return False

    def on_collision_with(self, entity: "Entity"):
        print(entity)
