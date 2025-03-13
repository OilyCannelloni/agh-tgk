from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import field

import pygame

from grid.position import *


class BaseSprite(pygame.sprite.Sprite):
    """
    Use this to create sprites for entities
    """
    def __init__(self, image: pygame.Surface, rect: pygame.rect.Rect):
        super().__init__()
        self.image = image
        self.rect = rect

    def update_position(self, pos: Position):
        self.rect.x = pos.x
        self.rect.y = pos.y


@dataclass
class Entity(ABC):
    """
    A base class for all entities
    """
    def __init__(self, position=None):
        self.position = position or Position(0, 0)

    @property
    @abstractmethod
    def sprite(self) -> BaseSprite:
        """
        Keeps the Sprite (the visual layer) of the entity.
        """
        pass


@dataclass
class GameTickAction:
    priority: int = 500
    action: Callable = field(default_factory=lambda: lambda: None)


class DynamicEntity(Entity, ABC):
    """
    An entity, which has a behavior which is performed every tick.
    """
    def __init__(self, position=None):
        super().__init__(position=position)
        self.game_tick_events: list[GameTickAction] = []

    def on_game_tick(self, **data):
        for gta in self.game_tick_events:
            gta.action(**data)

    def add_on_game_tick(self, action: Callable, priority: int) -> None:
        """
        Adds a behavior action to this entity's on-tick queue.
        :param action: The action
        :param priority: How early should the action be executed (0 = earliest)
        :return: None
        """
        index = 0
        while index < len(self.game_tick_events) and self.game_tick_events[index].priority < priority:
            index += 1
        self.game_tick_events.insert(index, GameTickAction(priority, action))


class MovableEntity(DynamicEntity, ABC):
    def __init__(self, position=None):
        super().__init__(position=position)
        self.add_on_game_tick(self.__update_sprite_position, 1000)

    def __update_sprite_position(self, **data):
        self.sprite.update_position(self.position)
