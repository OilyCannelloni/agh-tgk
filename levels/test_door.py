from entities.blocks import WallSegment
from entities.doors import OpenableDoor
from entities.entity_library import EntityLibrary
from entities.player import Player
from grid.position import Position
from levels.level import Level
from grid.grid import Grid

grid = Grid()

class LevelTestDoor(Level):
    def load(self):
        grid.place_existing_entity(WallSegment(Position(200, 0), Position(200, 100)))
        grid.place_existing_entity(WallSegment(Position(200, 150), Position(200, 500)))
        grid.place_existing_entity(WallSegment(Position(0, 500), Position(200, 500)))
        grid.place_existing_entity(OpenableDoor(Position(200, 100)))
        grid.place_existing_entity(Player(Position(100, 100)))