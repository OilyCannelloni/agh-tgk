from dataclasses import dataclass

import pygamepal as pp
from enum import Flag, Enum


class EntityType(Flag):
    DEFAULT = 0
    DYNAMIC = 1
    MOVABLE = 2
    PLAYER = 3


class HitboxType(Enum):
    MAIN = 0
    OTHER = 1


@dataclass
class TickData:
    pp_input: pp.Input

