from dataclasses import dataclass, field

import pygame

from entities.base import Entity, DynamicEntity
from .position import Position


@dataclass
class Grid:
    sprites = pygame.sprite.Group()
    dynamic_entities: list[DynamicEntity] = field(default_factory=list)

    def place_entity(self, entity: Entity, position: Position = None):
        if position is not None:
            entity.position = position
        self.sprites.add(entity.sprite)

        if isinstance(entity, DynamicEntity):
            self.dynamic_entities.append(entity)

    def process_dynamic_entities(self, **data):
        for entity in self.dynamic_entities:
            entity.on_game_tick(**data)