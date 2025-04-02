import inspect
from abc import ABC, abstractmethod
from collections.abc import Callable

import pygame

from entities.entity_library import EntityLibrary
from entities.types import EntityType
from grid.position import *
from grid.grid import Grid
from entities.types import EntityType
from ui.hint_renderer import hint_renderer
from hacking.hackable_method import HackableMethod
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


class Hitbox(pygame.Rect, ABC):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def move(self, x, y) -> 'Hitbox':
        new_hitbox = type(self)(
            self.x + x,
            self.y + y,
            self.width,
            self.height
        )
        return new_hitbox

    @abstractmethod
    def on_collision_with(self, e: "Entity") -> None:
        pass

    @abstractmethod
    def is_passable_for(self, e: "Entity") -> bool:
        pass


class PlayerInteractHitbox(Hitbox, ABC):
    def on_collision_with(self, e: "Entity") -> None:
        if e.type == EntityType.PLAYER:
            hint_renderer.show_hint()

    def is_passable_for(self, e: "Entity") -> bool:
        return True


class BlockingHitbox(Hitbox, ABC):
    def on_collision_with(self, e: "Entity") -> None:
        pass

    def is_passable_for(self, e: "Entity") -> bool:
        return False


@dataclass
class Entity(ABC):
    """
    A base class for all entities
    """
    type: EntityType = EntityType.DEFAULT

    def __init__(self, position=None, hitboxes=None):
        self.position = position or Position(0, 0)
        self.sprite = None
        EntityLibrary.register_entity(self.__class__.__name__, self.__class__)
        self.hitboxes = hitboxes or [BlockingHitbox(self.position.x, self.position.y, 20, 20)]

    def get_hitbox(self, hitbox_type: type):
        for hitbox in self.hitboxes:
            if isinstance(hitbox, hitbox_type):
                return hitbox

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
        new_hitboxes = [hb.move(vector.x, vector.y) for hb in self.hitboxes]
        new_interactable = None

        for new_hitbox in new_hitboxes:
            for target in grid.get_all_colliding_objects(new_hitbox):
                if target is self:
                    continue
                target.on_collision_with(self)
                self.on_collision_with(target)
                if not target.is_passable_for(self):
                    return

                if isinstance(target, InteractableEntity) and new_interactable is None:
                    new_interactable = target

        self.position = self.position.add(vector)
        for i in range(len(self.hitboxes)):
            self.hitboxes[i] = new_hitboxes[i]

        if new_interactable is None and (vector.x != 0 or vector.y != 0):
            hint_renderer.clear_hint()

    def __update_sprite_position(self, **data):
        self.sprite.update_position(self.position)


class InteractableEntity(Entity, ABC):
    def __init__(self, position=None, hitboxes=None):
        super().__init__(position, hitboxes=hitboxes or [PlayerInteractHitbox(self.position.x, self.position.y, 20, 20)])

    def on_collision_with(self, entity: "Entity"):
        for hb in self.hitboxes:
            hb.on_collision_with(entity)

    def is_passable_for(self, entity: "Entity"):
        for hb in self.hitboxes:
            if not hb.is_passable_for(entity):
                return False
        return True

class HackableEntity(DynamicEntity, ABC):
    """
    Describes an entity type the behavior of which can be altered by the user.
    """
    def __init__(self):
        super().__init__()
        self._terminal = Terminal()
        self._hackable_method_names = None

    def _get_hackable_method_names(self):
        if self._hackable_method_names is not None:
            return self._hackable_method_names
        self._hackable_method_names = list(HackableMethod.get_all_hackable_methods(self.__class__).keys())
        return self._hackable_method_names

    def display_hackable_methods(self):
        """
        Writes the current bodies of all hackable methods of the inheriting class
        onto the terminal
        """
        code = ""
        for name, method in HackableMethod.get_all_hackable_methods(self.__class__).items():
            code += "\n"
            source = inspect.getsource(method)
            code += source.strip().removeprefix("@HackableMethod")

        self._terminal.set_active_entity(self)
        self._terminal.set_code(code)

    def apply_code(self, code: str):
        """
        Applies the code from the terminal to overwrite the hackable methods of the inheriting class
        """
        HackableMethod.apply_code(code, self.__class__.__name__, self._get_hackable_method_names())
