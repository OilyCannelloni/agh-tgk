from abc import ABC
import pygame

from grid.position import *
from levels.base import Level
from .base import BaseSprite, MovableEntity
from entities.types import EntityType
import pygamepal as pp


@dataclass
class Player(MovableEntity, ABC):
    speed = 4

    def __init__(self, position=None):
        super().__init__(position=position, width=20, height=20, color="green")
        self.type |= EntityType.PLAYER
        self.add_on_game_tick(self.__get_movement_vector, 0)
        self.add_on_game_tick(self.__move, 100)
        self.current_movement_vector = Vector(0, 0)

    def __get_movement_vector(self, **data):
        pp_input: pp.Input = data.get("tick_data").pp_input
        if pp_input is None:
            self.current_movement_vector = Vector(0, 0)
            return

        vector = Vector(0, 0)
        if pp_input.isKeyDown(pygame.K_a):
            vector = vector.add(LEFT)
        if pp_input.isKeyDown(pygame.K_w):
            vector = vector.add(UP)
        if pp_input.isKeyDown(pygame.K_d):
            vector = vector.add(RIGHT)
        if pp_input.isKeyDown(pygame.K_s):
            vector = vector.add(DOWN)
        self.current_movement_vector = vector.scale(self.speed)

    def __move(self, **data):
        super().move(self.current_movement_vector)

    def killed_by(self, killer: str):
        print(f"You have been killed by {killer}")
        Level.load_last()

