from abc import ABC
import pygame

from grid.position import *
from .base import BaseSprite, MovableEntity


@dataclass
class Player(MovableEntity, ABC):
    speed = 3

    def __init__(self, position=None):
        super().__init__(position=position)
        self.add_on_game_tick(self.__get_movement_vector, 0)
        self.add_on_game_tick(self.__move, 100)

        self.sprite = BaseSprite(pygame.Surface([20, 20]), pygame.Rect(self.position.x, self.position.y, 20, 20))
        self.sprite.image.fill(pygame.color.Color("green"))
        self.current_movement_vector = Vector(0, 0)

    def __get_movement_vector(self, **data):
        if len(keys := data.get("keys_down", [])) == 0:
            self.current_movement_vector = Vector(0, 0)
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
        self.current_movement_vector = vector

    def __move(self, **data):
        super()._move(self.current_movement_vector)

