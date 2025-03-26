import functools
import inspect
import re
from abc import ABC
from collections import defaultdict
from collections.abc import Callable
from dataclasses import field
from typing import Any

import pygame

from random import random, randint

from functools import wraps

from entities.entity_library import EntityLibrary
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
        EntityLibrary.register_entity(self.__class__.__name__, self.__class__)

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


class HackableMethod:
    meth_info = defaultdict(dict)

    def __init__(self, meth: Callable):
        """
        Inserts the default body of a hackable method to meth_info dictionary.
        """
        self.class_name, self.meth_name = meth.__qualname__.rsplit('.', 1)
        print(self.class_name, self.meth_name)
        HackableMethod.meth_info[self.class_name][self.meth_name] = meth
        self._default_meth = meth

    def __call__(self, instance, owner, *args, **kwargs):
        """
        Overrides the decorated method call. Calls the version stored in meth_info instead.
        :param instance: Calling object instance
        :param owner: Calling object type
        :return: What the hacked method returns
        """
        return HackableMethod.meth_info[self.class_name][self.meth_name](instance, *args, **kwargs)

    def __get__(self, instance, owner):
        """
        Executes before __call__ when the method is called. Provides __call__ with access
        to the calling instance and type.
        """
        return functools.partial(self.__call__, instance, owner)

    @classmethod
    def get_all_hackable_methods(cls, owner_class):
        """
        Returns all hackable methods for a given type.
        :param owner_class: The type.
        :return: A dictionary of (method_name: method) pairs.
        """
        return cls.meth_info[owner_class.__name__]


class HackableEntity(DynamicEntity, ABC):
    def __init__(self):
        super().__init__()
        self._terminal = Terminal()
        self._hackable_method_names = None

    def get_hackable_methods(self):
        for name, method in HackableMethod.get_all_hackable_methods(self.__class__).items():
            yield name, method

    def _get_hackable_method_names(self):
        if self._hackable_method_names is not None:
            return self._hackable_method_names
        self._hackable_method_names = list(HackableMethod.get_all_hackable_methods(self.__class__).keys())
        return self._hackable_method_names

    def _overwrite_hackable_method_with_user_code(self, meth_name: str, meth: Callable):
        HackableMethod.meth_info[self.__class__.__name__][meth_name] = meth

    def display_hackable_methods(self):
        code = ""
        for name, method in self.get_hackable_methods():
            print(method)
            code += "\n"
            source = inspect.getsource(method)
            code += source.strip().removeprefix("@HackableMethod")

        self._terminal.set_active_entity(self)
        self._terminal.set_code(code)

    def apply_code(self, code: str):
        scope = {}
        # “As for the end of the universe...
        # I say let it come as it will, in ice, fire, or darkness.
        # What did the universe ever do for me that I should mind its welfare?”
        exec(code, None, scope)
        print(scope)
        for name, value in scope.items():
            if name in self._get_hackable_method_names():
                self._overwrite_hackable_method_with_user_code(name, value)
                print("axax")

        print(HackableMethod.meth_info)


