from dataclasses import dataclass

import pygame
import pygamepal as pp
from enum import Flag, Enum


class EntityType(Flag):
    DEFAULT = 0
    DYNAMIC = 1
    MOVABLE = 2
    PLAYER = 4
    HACKABLE = 8
    INTERACTABLE = 16
    KILLABLE = 32


class HitboxType(Enum):
    MAIN = 0
    OTHER = 1


@dataclass
class TickData:
    tick: int = 0
    pp_input: pp.Input = None


class FRect(pygame.Rect):
    def __init__(self, fx, fy, w, h):
        self.fx = fx
        self.fy = fy
        super().__init__(round(fx), round(fy), w, h)

    def move_ip(self, x, y, /):
        self.fx += x
        self.fy += y
        super().update(round(self.fx), round(self.fy), self.width, self.height)

    def move(self, x, y, /):
        return FRect(self.fx + x, self.fy + y, self.width, self.height)