from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pygame
import pygamepal as pp

from entities.entity_library import EntityLibrary
from .position import Position
from entities.types import EntityType, TickData

if TYPE_CHECKING:
    from entities.base import Entity, DynamicEntity, InteractableEntity, HackableEntity


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

    def register_entity(self, entity: "Entity"):
        """
        Places a previously created entity on the map
        :param entity: The entity to be placed
        :param position: Position on the map
        """

        self.entities.append(entity)
        if EntityType.DYNAMIC in entity.type:
            self.dynamic_entities.append(entity)

    def place_entity_by_name(self, entity_name: str, position: "Position" = None, **kwargs):
        """
        Creates and places an entity on the map
        :param entity_name: Name of the entity as registered in EntityLibrary
        :param position: Position on the map
        :param kwargs: Parameters to be passed to the entity
        """
        entity = EntityLibrary.create_entity(entity_name, position=position, **kwargs)
        self.register_entity(entity)

    def clear(self):
        """
        Removes all entities
        """
        self.sprites = pygame.sprite.Group()
        self.dynamic_entities = []
        self.entities = []
        self.current_interactable_entity = None

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

    def process_player_input(self, tick_data: TickData):
        """
        Responds to player actions other than movement
        """
        if tick_data.pp_input.isKeyPressed(pygame.K_e):
            if (self.current_interactable_entity is not None
                        and EntityType.INTERACTABLE in self.current_interactable_entity.type):
                self.current_interactable_entity.on_player_interaction(tick_data)

        if tick_data.pp_input.isKeyPressed(pygame.K_t):
            if EntityType.HACKABLE in self.current_interactable_entity.type:
                self.current_interactable_entity: HackableEntity
                self.current_interactable_entity.display_special_methods()

    def remove_entity(self, entity):
        self.sprites.remove(entity.sprite)
        self.entities.remove(entity)
        if EntityType.DYNAMIC in entity.type:
            self.dynamic_entities.remove(entity)

