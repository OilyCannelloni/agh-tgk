from abc import ABC
import pygame

from grid.position import *
from .base import BaseSprite, MovableEntity


@dataclass
class Player(MovableEntity, ABC):
    speed = 3

    def __init__(self, position=None):
        super().__init__(position=position)
        self.add_on_game_tick(self.__move, 0)
        self._sprite = BaseSprite(pygame.Surface([20, 20]), pygame.Rect(self.position.x, self.position.y, 20, 20))
        self._sprite.image.fill(pygame.color.Color("green"))

    @property
    def sprite(self):
        return self._sprite

    def __move(self, **data):
        if len(keys := data.get("keys_down", [])) == 0:
            return

        MOVE_KEYS = (pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_UP)
        vector = Vector(0, 0)
        for key in keys:
            if key not in MOVE_KEYS:
                continue
            match key:
                case pygame.K_LEFT:
                    vector = vector.add(LEFT)
                case pygame.K_DOWN:
                    vector = vector.add(DOWN)
                case pygame.K_RIGHT:
                    vector = vector.add(RIGHT)
                case _:
                    vector = vector.add(UP)
        self.position = self.position.add(vector.scale(self.speed))
