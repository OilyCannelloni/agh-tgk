from dataclasses import dataclass

import pygamepal as pp
from enum import Flag, Enum


class EntityType(Flag):
    DEFAULT = 0
    DYNAMIC = 1
    MOVABLE = 2
    PLAYER = 4
    HACKABLE = 8
    INTERACTABLE = 16


class HitboxType(Enum):
    MAIN = 0
    OTHER = 1


@dataclass
class TickData:
    tick: int = 0
    pp_input: pp.Input = None

