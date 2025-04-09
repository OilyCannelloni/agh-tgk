import inspect
from abc import ABC, abstractmethod
from collections.abc import Callable

import pygame

from entities.entity_library import EntityLibrary
from grid.position import *
from grid.grid import Grid
from entities.types import EntityType, TickData, HitboxType
from ui.hint_renderer import hint_renderer
from hacking.hackable_method import HackableMethod
from terminal.terminal import Terminal

grid = Grid()


class BaseSprite(pygame.sprite.Sprite):
    """
    Use this to create sprites for entities
    """
    def __init__(self, *, image: pygame.Surface, rect: pygame.rect.Rect):
        super().__init__()
        self.image = image
        self.rect = rect

    def update_position(self, pos: Position):
        self.rect.x = pos.x
        self.rect.y = pos.y


class Hitbox(pygame.Rect, ABC):
    def __init__(self, *, owner: "Entity", x, y, width, height):
        super().__init__(x, y, width, height)
        self.owner = owner

    def move(self, x, y) -> 'Hitbox':
        new_hitbox = type(self)(
            owner=self.owner,
            x=self.x + x,
            y=self.y + y,
            width=self.width,
            height=self.height
        )
        return new_hitbox

    @abstractmethod
    def on_collision_with(self, e: "Entity") -> None:
        pass

    @abstractmethod
    def is_passable_for(self, e: "Entity") -> bool:
        pass


class MainHitbox(Hitbox, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = HitboxType.MAIN

    def on_collision_with(self, e: "Entity") -> None:
        self.owner.on_collision_with(e)

    def is_passable_for(self, e: "Entity") -> bool:
        return False


class PlayerInteractHitbox(Hitbox, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert isinstance(self.owner, InteractableEntity)
        self.type = HitboxType.OTHER

    def on_collision_with(self, e: "Entity") -> None:
        if EntityType.PLAYER in e.type:
            hint_renderer.show_hint()
            grid.current_interactable_entity = self.owner

    def is_passable_for(self, e: "Entity") -> bool:
        return True


@dataclass
class Entity(ABC):
    """
    A base class for all entities
    """
    type: EntityType = EntityType.DEFAULT

    def __init__(self, *, position=None, main_hitbox=None, hitboxes=None):
        self.position = position or Position(0, 0)
        self.sprite = None
        EntityLibrary.register_entity(self.__class__.__name__, self.__class__)

        self.main_hitbox = main_hitbox or MainHitbox(owner=self,
                                            x=self.position.x, y=self.position.y, width=20, height=20)
        self.hitboxes = hitboxes or []

    def get_hitbox(self, hitbox_type: type):
        for hitbox in self.hitboxes:
            if isinstance(hitbox, hitbox_type):
                return hitbox

    def get_hitboxes(self):
        return self.main_hitbox, *self.hitboxes

    def is_passable_for(self, entity: "Entity"):
        return False

    def on_collision_with(self, entity: "Entity"):
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_tick_events: list[GameTickAction] = []

    def on_game_tick(self, tick_data: TickData):
        """
        Runs all actions assigned to this entity in order of their priority
        :param tick_data: Information about the current tick
        """
        for gta in self.game_tick_events:
            gta.action(tick_data=tick_data)

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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = super().type | EntityType.MOVABLE
        self.add_on_game_tick(self.__update_sprite_position, 1000)

    def _move(self, vector: Vector):
        new_main_hitbox = self.main_hitbox.move(vector.x, vector.y)
        interactable_found = False

        for target_hb in grid.get_all_colliding_hitboxes(new_main_hitbox):
            if target_hb.owner is self:
                continue
            target_hb.on_collision_with(self)
            if target_hb.type == HitboxType.MAIN:
                self.on_collision_with(target_hb.owner)
                if not target_hb.owner.is_passable_for(self):
                    return

            if EntityType.INTERACTABLE in target_hb.owner.type:
                interactable_found = True

        self.position = self.position.add(vector)
        self.main_hitbox.move_ip(vector.x, vector.y)
        for i in range(len(self.hitboxes)):
            self.hitboxes[i].move_ip(vector.x, vector.y)

        # TODO: Move everything connected with player's interaction to Player class
        # As for now we can't make drones
        if not interactable_found:
            hint_renderer.clear_hint()

    def __update_sprite_position(self, **kwargs):
        self.sprite.update_position(self.position)


class InteractableEntity(Entity, ABC):
    def __init__(self, *, position=None, hitboxes=None, interact_hitbox: PlayerInteractHitbox = None, **kwargs):
        if hitboxes is None:
            hitboxes = []

        # TODO this should depend on self.height/width
        hitboxes.append(interact_hitbox or PlayerInteractHitbox(
                                    owner=self,
                                    x=position.x - 5, y=position.y - 5, width=30, height=30))
        super().__init__(position=position, hitboxes=hitboxes, **kwargs)
        self.type |= EntityType.INTERACTABLE

    @abstractmethod
    def on_player_interaction(self):
        """
        This method is called when the player presses E while near this entity.
        :return:
        """
        pass



class HackableEntity(DynamicEntity, ABC):
    """
    Describes an entity type the behavior of which can be altered by the user.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type |= EntityType.HACKABLE
        self._terminal = Terminal()
        self._hackable_method_names = None

    def get_hackable_method_names(self):
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
        HackableMethod.apply_code(code, self)
