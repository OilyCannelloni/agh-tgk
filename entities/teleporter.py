import pygame

from entities.base import Entity, DynamicEntity, MovableEntity
from entities.types import EntityType
from grid.position import Position


class TeleporterTarget(Entity):
    def __init__(self, position: Position):
        super().__init__(position=position, width=30, height=30, color=pygame.Color(200, 200, 0, 100))

    def is_passable_for(self, entity: "Entity"):
        return True


class Teleporter(Entity):
    def __init__(self, position: Position):
        super().__init__(position=position, width=30, height=30, color=pygame.Color("magenta"))
        self.target: TeleporterTarget = None

    def set_target(self, target: TeleporterTarget):
        self.target = target

    def on_collision_with(self, entity: "Entity"):
        if self.target is not None and EntityType.PLAYER in entity.type:
            entity: MovableEntity
            entity.move_to(self.target.position)


