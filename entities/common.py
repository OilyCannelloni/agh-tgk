from typing import Callable

import pygame.image

from entities.base import Entity
from grid.position import Position
from utils import load_icon


class Exit(Entity):
    def __init__(self, position: Position, on_exit: Callable):
        width = 30
        height = 40
        image = load_icon(width, height, "resources/door-open.png", "cyan")
        super().__init__(position=position, width=width, height=height, color="cyan", custom_image=image)
        self.on_exit = on_exit

    def on_collision_with(self, entity: "Entity"):
        self.on_exit()
