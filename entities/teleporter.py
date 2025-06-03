from collections.abc import Callable

import pygame

from entities.base import Entity, DynamicEntity, MovableEntity, HackableEntity
from entities.types import EntityType
from grid.grid import Grid
from grid.position import Position
from hacking.hackable_method import HackableMethod, CallableMethod, ReadOnlyMethod
from utils import load_icon

TELEPORTER_IMAGE_PATH = "resources/teleport.png"


class TeleporterTarget(Entity):
    def __init__(self, position: Position, **kwargs):
        width = height = 15
        image = load_icon(width, height, TELEPORTER_IMAGE_PATH, (200, 200, 0))
        super().__init__(position=position, width=width, height=height, color=pygame.Color(200, 200, 0, 100), custom_image=image, **kwargs)

    def is_passable_for(self, entity: "Entity"):
        return True


class Teleporter(Entity):
    def __init__(self, position: Position, **kwargs):
        width = height = 30
        image = load_icon(width, height, TELEPORTER_IMAGE_PATH, "magenta")
        super().__init__(position=position, width=width, height=height, color=pygame.Color("magenta"),
                         custom_image=image, **kwargs)
        self.target: TeleporterTarget = None

    def set_target(self, target: TeleporterTarget):
        self.target = target

    def on_collision_with(self, entity: "Entity"):
        if self.target is not None and EntityType.PLAYER in entity.type:
            entity: MovableEntity
            entity.move_to(self.target.position)


class HackableTeleporter(Teleporter, HackableEntity):
    def __init__(self, position: Position, targets: list[TeleporterTarget], teleporters: list[Teleporter], **kwargs):
        super().__init__(position=position, interaction_offset=15, **kwargs)
        self.targets = targets
        self.other_teleporters = teleporters

    @CallableMethod
    def set_target(self, target):
        self.target = target

    @CallableMethod
    def get_valid_targets(self):
        return self.targets

    @CallableMethod
    def get_other_teleporters(self):
        return self.other_teleporters
