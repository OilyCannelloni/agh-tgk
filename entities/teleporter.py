from collections.abc import Callable

import pygame

from entities.base import Entity, DynamicEntity, MovableEntity, HackableEntity
from entities.types import EntityType
from grid.position import Position
from hacking.hackable_method import HackableMethod, CallableMethod, ReadOnlyMethod


class TeleporterTarget(Entity):
    def __init__(self, position: Position, **kwargs):
        super().__init__(position=position, width=30, height=30, color=pygame.Color(200, 200, 0, 100), **kwargs)

    def is_passable_for(self, entity: "Entity"):
        return True


class Teleporter(Entity):
    def __init__(self, position: Position, **kwargs):
        super().__init__(position=position, width=30, height=30, color=pygame.Color("magenta"), **kwargs)
        self.target: TeleporterTarget = None

    def set_target(self, target: TeleporterTarget):
        self.target = target

    def on_collision_with(self, entity: "Entity"):
        if self.target is not None and EntityType.PLAYER in entity.type:
            entity: MovableEntity
            entity.move_to(self.target.position)


class HackableTeleporter(Teleporter, HackableEntity):
    def __init__(self, position: Position, **kwargs):
        super().__init__(position=position, interaction_offset=15)
    
    @CallableMethod
    def set_target(self, target: TeleporterTarget):
        self.target = target

    @HackableMethod
    def dopa(self):
        pass

    @ReadOnlyMethod
    def syff(self):
        pass

