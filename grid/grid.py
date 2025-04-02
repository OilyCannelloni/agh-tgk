from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pygame
import pygamepal as pp

from entities.entity_library import EntityLibrary
from .position import Position
from entities.types import EntityType, TickData

if TYPE_CHECKING:
    from entities.base import Entity, DynamicEntity, InteractableEntity


@dataclass
class Grid:
    sprites = pygame.sprite.Group()
    dynamic_entities: list["DynamicEntity"] = field(default_factory=list)
    entities: list["Entity"] = field(default_factory=list)

    current_interactable_entity: "InteractableEntity" = None

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def place_existing_entity(self, entity: "Entity", position: "Position" = None):
        """
        Places a previously created entity on the map
        :param entity: The entity to be placed
        :param position: Position on the map
        """
        if position is not None:
            entity.position = position
        self.sprites.add(entity.sprite)

        self.entities.append(entity)
        if entity.type & EntityType.DYNAMIC:
            self.dynamic_entities.append(entity)

    def place_entity(self, entity_name: str, position: "Position" = None, **kwargs):
        """
        Creates and places an entity on the map
        :param entity_name: Name of the entity as registered in EntityLibrary
        :param position: Position on the map
        :param kwargs: Parameters to be passed to the entity
        """
        entity = EntityLibrary.create_entity(entity_name, **kwargs)
        self.place_existing_entity(entity, position)

    def process_dynamic_entities(self, tick_data: TickData):
        """
        Calls all tick actions for all dynamic entities.
        :param tick_data: Information about the current tick
        """
        for entity in self.dynamic_entities:
            entity.on_game_tick(tick_data)

    def get_all_colliding_hitboxes(self, hitbox):
        """
        Iterates over all registered hitboxes of entities, which collide with the given one
        :param hitbox: A hitbox of the origin
        """
        for e in self.entities:
            for target_hb in e.get_hitboxes():
                if hitbox.colliderect(target_hb):
                    yield target_hb

    def process_player_input(self, key_input: pp.Input):
        """
        Responds to player actions other than movement
        """
        if key_input.isKeyPressed(pygame.K_e):
            if self.current_interactable_entity is not None:
                self.current_interactable_entity.on_player_interaction()

        if key_input.isKeyPressed(pygame.K_t):
            print("TTT")
