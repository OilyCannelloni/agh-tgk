import random
from abc import ABC

from entities.blocks import WallSegment, Trap
from entities.common import Exit
from entities.doors import OpenableDoor, HackableDoorButton, DestroyButton
from entities.laser import LaserEmitter, Zombie
from entities.player import Player
from entities.teleporter import TeleporterTarget, Teleporter, HackableTeleporter
from grid.position import Position, Vector
from levels.base import Level



class LevelTestDoor(Level):
    @classmethod
    def load(cls):
        super().load()
        WallSegment(Position(200, 0), Position(200, 100))
        WallSegment(Position(200, 150), Position(200, 500))
        WallSegment(Position(10, 500), Position(200, 500))
        door = OpenableDoor(Position(200, 100))
        button = HackableDoorButton(Position(100, 400))
        button.set_target_door(door)
        Player(Position(100, 100))
        Exit(Position(300, 200), LevelTeleporter.load)


class LevelTeleporter(Level):
    """
ts = self.get_valid_targets()
tps = self.get_other_teleporters()

min_y = 999
for tp in tps:
    if tp.target.position.y < min_y:
        min_y = tp.target.position.y
        exit_tp = tp

ey = exit_tp.position.y
for target in ts:
    y = target.position.y
    if 40 < ey - y < 60:
        exit_target = target

self.set_target(exit_target)
    """

    @staticmethod
    def make_middle_cell(position, target):
        Level.make_wall_cell("nesw", 100, position)
        tel = Teleporter(position + Vector(10, 10))
        tel.set_target(target)
        in_target = TeleporterTarget(position + Vector(-40, -40))
        return in_target, tel

    @staticmethod
    def make_trap_cell(position):
        Level.make_wall_cell("nesw", 100, position)
        tt = TeleporterTarget(position + Vector(-40, -40))
        Trap(position + Vector(10, 10))
        return tt

    @staticmethod
    def make_exit_cell(position):
        Level.make_wall_cell("nesw", 100, position)
        tt = TeleporterTarget(position + Vector(-40, -40))
        Exit(position + Vector(10, 0), LevelLasers.load)
        return tt

    @classmethod
    def load(cls):
        super().load()
        Player(Position(100, 100))

        exit_tt = LevelTeleporter.make_exit_cell(Position(450, 200))
        trap_tt = LevelTeleporter.make_trap_cell(Position(450, 350))

        mid_cell_positions = [0, 1, 2, 3]
        exit_mid_cell_position = random.choice(mid_cell_positions)
        mid_cell_positions.remove(exit_mid_cell_position)

        trap_mid_tts = []
        other_teleporters = []
        for x in mid_cell_positions:
            in_tt, other_tp = LevelTeleporter.make_middle_cell(Position(300, 130 * x + 80), trap_tt)
            trap_mid_tts.append(in_tt)
            other_teleporters.append(other_tp)

        exit_mid_tt, exit_mid_tp = LevelTeleporter.make_middle_cell(Position(300, 130*exit_mid_cell_position + 80), exit_tt)

        all_tts = [*trap_mid_tts, exit_mid_tt]
        random.shuffle(all_tts)
        other_teleporters.append(exit_mid_tp)
        random.shuffle(other_teleporters)

        tel = HackableTeleporter(Position(200, 200), all_tts, other_teleporters)
        tel.set_target(random.choice(trap_mid_tts))


class LevelLasers(Level, ABC):
    @classmethod
    def load(cls):
        super().load()
        p = Player(Position(100, 100))
        LaserEmitter(Position(200, 150), delay=25)

        w = WallSegment(Position(0, 550), Position(300, 550))
        d = DestroyButton(Position(100, 150))
        d.set_target(w)


        for i in range(200, 300, 15):
            z = Zombie(Position(i, 600))
            z.set_target(p)

        Exit(Position(50, 570), LevelLasers.load)