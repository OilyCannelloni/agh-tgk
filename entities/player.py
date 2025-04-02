from abc import ABC
import pygame

from grid.position import *
from .base import BaseSprite, MovableEntity


@dataclass
class Player(MovableEntity, ABC):
    speed = 4

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

        vector = Vector(0, 0)
        if keys[pygame.K_a]:
            vector = vector.add(LEFT)
        if keys[pygame.K_w]:
            vector = vector.add(UP)
        if keys[pygame.K_d]:
            vector = vector.add(RIGHT)
        if keys[pygame.K_s]:
            vector = vector.add(DOWN)
        self.current_movement_vector = vector.scale(self.speed)

    def __move(self, **data):
        super()._move(self.current_movement_vector)

