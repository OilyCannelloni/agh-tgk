import inspect
from abc import ABC
from collections.abc import Callable
from dataclasses import field
from typing import Any

import pygame

from functools import wraps
from grid.position import *
from grid.grid import Grid
from entities.types import EntityType
from terminal.terminal import Terminal

grid = Grid()


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
    type: EntityType = EntityType.DEFAULT

    def __init__(self, position=None, hitbox=None):
        self.position = position or Position(0, 0)
        self.sprite = None
        self.hitbox = hitbox or pygame.Rect(self.position.x, self.position.y, 20, 20)

    def on_collision_with(self, entity: "Entity"):
        pass

    def is_passable_for(self, entity: "Entity"):
        pass


@dataclass
class GameTickAction:
    priority: int
    action: Callable


class DynamicEntity(Entity, ABC):
    """
    An entity, which has a behavior which is performed every tick.
    """
    type = EntityType.DYNAMIC

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
    type = EntityType.DYNAMIC | EntityType.MOVABLE

    def __init__(self, position=None):
        super().__init__(position=position)
        self.add_on_game_tick(self.__update_sprite_position, 1000)

    def _move(self, vector: Vector):
        new_hitbox = self.hitbox.move(vector.x, vector.y)
        for target in grid.get_all_colliding_objects(new_hitbox):
            if target is self:
                continue
            target.on_collision_with(self)
            self.on_collision_with(target)
            if not target.is_passable_for(self):
                return

        self.position = self.position.add(vector)
        self.hitbox = new_hitbox

    def __update_sprite_position(self, **data):
        self.sprite.update_position(self.position)


class HackableEntity(DynamicEntity, ABC):
    def __init__(self):
        super().__init__()
        self.terminal = Terminal()

    @staticmethod
    def hackable(f):
        @wraps(f)
        def wrapper(self: HackableEntity, **kwargs):
            print("hvo")
            f(self, **kwargs)
        return wrapper


    def _expose_hackable_method(self, func: Callable):
        code = inspect.getsource(func)
        self.terminal.set_text_from_string(code)

    def _apply_hacked_method_body(self, func: Callable, code: str):
        pass
