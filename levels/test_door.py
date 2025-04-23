from entities.blocks import WallSegment
from entities.doors import OpenableDoor, DoorButton
from entities.entity_library import EntityLibrary
from entities.player import Player
from grid.position import Position
from levels.level import Level
from grid.grid import Grid

grid = Grid()

class LevelTestDoor(Level):
    @staticmethod
    def load():
        grid.place_existing_entity(WallSegment(Position(200, 0), Position(200, 100)))
        grid.place_existing_entity(WallSegment(Position(200, 150), Position(200, 500)))
        grid.place_existing_entity(WallSegment(Position(10, 500), Position(200, 500)))
        door = OpenableDoor(Position(200, 100))
        grid.place_existing_entity(door)
        button = DoorButton(Position(100, 400))
        button.set_target_door(door)
        grid.place_existing_entity(button)
        grid.place_existing_entity(Player(Position(100, 100)))