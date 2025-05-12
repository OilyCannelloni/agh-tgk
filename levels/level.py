from abc import ABC, abstractmethod
from entities.blocks import WallSegment
from entities.common import Exit
from entities.doors import OpenableDoor, DoorButton
from entities.player import Player
from entities.teleporter import TeleporterTarget, Teleporter, HackableTeleporter
from grid.position import Position
from grid.grid import Grid


class Level(ABC):
    @staticmethod
    @abstractmethod
    def load():
        pass


grid = Grid()


class LevelTestDoor(Level):
    @staticmethod
    def load():
        grid.clear()
        WallSegment(Position(200, 0), Position(200, 100))
        WallSegment(Position(200, 150), Position(200, 500))
        WallSegment(Position(10, 500), Position(200, 500))
        door = OpenableDoor(Position(200, 100))
        button = DoorButton(Position(100, 400))
        button.set_target_door(door)
        Player(Position(100, 100))
        Exit(Position(300, 200), LevelTestDoor.load)


class LevelTeleporter(Level):
    @staticmethod
    def load():
        Player(Position(100, 100))

        tt = TeleporterTarget(Position(200, 400))

        tel = HackableTeleporter(Position(200, 200))
        print(tel.type)
        tel.set_target(tt)

