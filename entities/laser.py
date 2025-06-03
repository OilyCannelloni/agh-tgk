import pygame

from entities.base import DynamicEntity, MovableEntity, Entity
from entities.types import EntityType
from grid.position import Vector, Position
from utils import load_icon


class LaserEmitter(DynamicEntity):
    def __init__(self, position: Position, delay: int = 50, **kwargs):
        width = height = 40
        image = load_icon(width, height, "resources/cannon.png", "grey")

        super().__init__(position=position, width=width, height=height, color="gray", custom_image=image, **kwargs)
        self.delay = delay
        self.add_on_game_tick(self._decide_shoot_laser, 100)

    def _decide_shoot_laser(self, tick_data):
        if tick_data.tick % self.delay == 0:
            self.shoot_laser()

    def shoot_laser(self):
        LaserBullet(position=self.position + Position(self.width - 10, self.height - 10))

    def is_passable_for(self, entity: "Entity"):
        if isinstance(entity, LaserBullet):
            return True
        return False


class LaserBullet(MovableEntity):
    def __init__(self, *, vector=Vector(4, 4), **kwargs):
        super().__init__(color="cyan", width=5, height=5, **kwargs)
        self.vector = vector
        self.add_on_game_tick(self.__move, 100)

    def __move(self, tick_data):
        super().move(self.vector)

    def on_collision_with(self, entity: "Entity"):
        if EntityType.KILLABLE in entity.type:
            entity.killed_by("bullet")


class NaiveChasingEntity(MovableEntity):
    def __init__(self, speed: int = 3, **kwargs):
        super().__init__(**kwargs)
        self.target_entity: Entity = None
        self.vector = Vector(0, 0)
        self.speed = speed
        self.add_on_game_tick(self.get_movement_vector, 10)
        self.add_on_game_tick(self.__move, 100)

    def set_target(self, entity: Entity):
        self.target_entity = entity

    def get_movement_vector(self, tick_data):
        if self.target_entity is None:
            self.vector = Vector(0, 0)
            return
        dx = self.target_entity.position.x - self.position.x
        dy = self.target_entity.position.y - self.position.y
        self.vector = Vector(dx, dy).normalize().scale(self.speed)

    def __move(self, tick_data):
        super().move(self.vector)


class Zombie(NaiveChasingEntity):
    def __init__(self, position: Position):
        width = height = 15
        image = load_icon(width, height, "resources/zombie.png", "brown")

        super().__init__(speed=5, position=position, width=width, height=height, color="brown", custom_image=image)
        self.type |= EntityType.KILLABLE

    def on_collision_with(self, entity: "Entity"):
        if EntityType.PLAYER in entity.type:
            entity.killed_by("zombie")
