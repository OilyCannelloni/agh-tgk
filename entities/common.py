from typing import Callable

import pygame.image

from entities.base import Entity
from grid.position import Position


class Exit(Entity):
    def __init__(self, position: Position, on_exit: Callable):
        super().__init__(position=position, width=30, height=50, color="cyan")
        self.on_exit = on_exit
        # TODO make this image work
        # self.sprite.image = pygame.image.load("resources/exit.png")

    def on_collision_with(self, entity: "Entity"):
        self.on_exit()