from entities.base import DynamicEntity, InteractableEntity, HackableEntity
from entities.types import TickData
from grid.position import Position
from hacking.hackable_method import HackableMethod


class BasicDoor(DynamicEntity):
    THICKNESS = 10

    def __init__(self, position: Position, **kwargs):
        super().__init__(position=position, width=BasicDoor.THICKNESS, height=50, color="orange", **kwargs)
        self.is_open = False

    def open(self):
        if self.is_open:
            return
        self.set_size(self.height, self.width)
        self.is_open = True

    def close(self):
        if not self.is_open:
            return
        self.set_size(self.height, self.width)
        self.is_open = False


class OpenableDoor(BasicDoor, InteractableEntity):
    def on_player_interaction(self, tick_data: TickData):
        if self.is_open:
            self.close()
        else:
            self.open()


class DoorButton(InteractableEntity, HackableEntity):
    def __init__(self, position: Position, **kwargs):
        super().__init__(position=position, width=30, height=30, color="orange", **kwargs)
        self.door: BasicDoor = None
        self.release_tick = -1
        self.add_on_game_tick(self.on_tick, 600)

    def set_target_door(self, door: BasicDoor):
        self.door = door

    def unclick(self):
        if self.door is not None:
            self.door.close()

    def click(self):
        if self.door is not None:
            self.door.open()

    @HackableMethod
    def on_player_interaction(self, tick_data):
        self.release_tick = tick_data.tick + 50
        self.click()

    def on_tick(self, tick_data: TickData):
        if tick_data.tick == self.release_tick:
            self.unclick()


