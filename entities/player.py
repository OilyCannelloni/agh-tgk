from abc import ABC
import pygame

from grid.grid import Grid
from grid.position import *
from utils import tint_image
from levels.base import Level
from ui.hint_renderer import GameHintRenderer
from .base import MovableEntity
from entities.types import EntityType, HitboxType
import pygamepal as pp

grid = Grid()
hint_renderer = GameHintRenderer()


@dataclass
class Player(MovableEntity, ABC):
    speed = 4

    def __init__(self, position=None):
        width = height = 30
        image = pygame.image.load("resources/character.png").convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        image = tint_image(image, "green")

        super().__init__(position=position, width=width, height=height, color="green", custom_image=image)
        self.type |= EntityType.PLAYER | EntityType.KILLABLE
        self.add_on_game_tick(self.__get_movement_vector, 0)
        self.add_on_game_tick(self.__move, 100)
        self.current_movement_vector = Vector(0, 0)

    def __get_movement_vector(self, **data):
        pp_input: pp.Input = data.get("tick_data").pp_input
        if pp_input is None:
            self.current_movement_vector = Vector(0, 0)
            return

        vector = Vector(0, 0)
        if pp_input.isKeyDown(pygame.K_a):
            vector = vector.add(LEFT)
        if pp_input.isKeyDown(pygame.K_w):
            vector = vector.add(UP)
        if pp_input.isKeyDown(pygame.K_d):
            vector = vector.add(RIGHT)
        if pp_input.isKeyDown(pygame.K_s):
            vector = vector.add(DOWN)
        self.current_movement_vector = vector.scale(self.speed)

    def __move(self, **data):
        self.move(self.current_movement_vector)

    def move(self, vector: Vector):
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

            if EntityType.INTERACTABLE in target_hb.owner.type or EntityType.HACKABLE in target_hb.owner.type:
                interactable_found = True

        self.position = self.position + vector
        self.main_hitbox.move_ip(vector.x, vector.y)
        for i in range(len(self.hitboxes)):
            self.hitboxes[i].move_ip(vector.x, vector.y)

        if not interactable_found:
            hint_renderer.clear_hint()

    def killed_by(self, killer: str):
        print(f"You have been killed by {killer}")
        Level.load_last()

