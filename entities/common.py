from typing import Callable

import pygame.image

from entities.base import Entity
from grid.position import Position
from utils import tint_image


class Exit(Entity):
    def __init__(self, position: Position, on_exit: Callable):
        width = 30
        height = 40
        image = self._load_icon(width, height)
        super().__init__(position=position, width=width, height=height, color="cyan", custom_image=image)
        self.on_exit = on_exit

    @staticmethod
    def _load_icon(width, height):
        try:
            image = pygame.image.load("resources/door-open.png").convert_alpha()
        except pygame.error as e:
            raise RuntimeError(f"Failed to load teleporter image: {e}")
        image = pygame.transform.scale(image, (width, height))
        image = tint_image(image, "cyan")
        return image

    def on_collision_with(self, entity: "Entity"):
        self.on_exit()
