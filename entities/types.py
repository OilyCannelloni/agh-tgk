from enum import Flag


class EntityType(Flag):
    DEFAULT = 0
    DYNAMIC = 1
    MOVABLE = 2
    PLAYER = 3
