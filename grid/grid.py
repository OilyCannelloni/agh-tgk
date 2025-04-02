from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pygame

from entities.entity_library import EntityLibrary
from .position import Position
from entities.types import EntityType

if TYPE_CHECKING:
    from entities.base import Entity, DynamicEntity


@dataclass
class Grid:
    sprites = pygame.sprite.Group()
    dynamic_entities: list["DynamicEntity"] = field(default_factory=list)
    entities: list["Entity"] = field(default_factory=list)

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def place_existing_entity(self, entity: "Entity", position: "Position" = None):
        if position is not None:
            entity.position = position
        self.sprites.add(entity.sprite)

        self.entities.append(entity)
        if entity.type & EntityType.DYNAMIC:
            self.dynamic_entities.append(entity)

    def place_entity(self, entity_name: str, *args, position: "Position" = None, **kwargs):
        entity = EntityLibrary.create_entity(entity_name, *args, **kwargs)
        self.place_existing_entity(entity, position)

    def process_dynamic_entities(self, **data):
        for entity in self.dynamic_entities:
            entity.on_game_tick(**data)

    def get_all_colliding_objects(self, hitbox):
        for e in self.entities:
            if hitbox.colliderect(e.hitbox):
                yield e
