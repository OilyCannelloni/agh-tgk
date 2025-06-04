from entities.base import DynamicEntity, InteractableEntity, HackableEntity, Entity
from entities.types import TickData
from grid.position import Position
from hacking.hackable_method import HackableMethod
from utils import load_icon, create_surface


class BasicDoor(DynamicEntity):
    THICKNESS = 10
    ICON_PATH = "resources/wood.png"

    def __init__(self, position: Position, **kwargs):

        height=50
        door = create_surface(BasicDoor.THICKNESS, height, BasicDoor.ICON_PATH, BasicDoor.THICKNESS)
        super().__init__(position=position, width=BasicDoor.THICKNESS, height=height, custom_image=door, **kwargs)
        self.is_open = False

    def open(self):
        if self.is_open:
            return
        door = create_surface(self.height, self.width, BasicDoor.ICON_PATH, BasicDoor.THICKNESS)
        self.set_size(self.height, self.width, door)
        self.is_open = True

    def close(self):
        if not self.is_open:
            return
        door = create_surface(self.height, self.width, BasicDoor.ICON_PATH, BasicDoor.THICKNESS)
        self.set_size(self.height, self.width, door)
        self.is_open = False


class OpenableDoor(BasicDoor, InteractableEntity):
    def on_player_interaction(self, tick_data: TickData):
        if self.is_open:
            self.close()
        else:
            self.open()


class DestroyButton(InteractableEntity):
    def __init__(self, position: Position, **kwargs):
        width = height = 30
        image = load_icon(width, height, "resources/lever.png", "orange")

        super().__init__(position=position, width=30, height=30, color="orange", custom_image=image, **kwargs)
        self.target: Entity = None

    def set_target(self, entity: Entity):
        self.target = entity

    def on_player_interaction(self, tick_data):
        image = load_icon(self.width, self.height, "resources/lever-mirror.png", "orange")
        self.set_sprite("orange", image)
        self.target.destroy()



class HackableDoorButton(InteractableEntity, HackableEntity):
    def __init__(self, position: Position, **kwargs):
        width=height=30
        image = load_icon(width, height, "resources/lever.png", "orange")
        super().__init__(position=position, width=width, height=height, color="orange", custom_image=image, **kwargs)
        self.door: BasicDoor = None
        self.release_tick = -1
        self.add_on_game_tick(self.on_tick, 600)

    def set_target_door(self, door: BasicDoor):
        self.door = door

    def unclick(self):
        image = load_icon(self.width, self.height, "resources/lever.png", "orange")
        self.set_sprite("orange", image)
        if self.door is not None:
            self.door.close()

    def click(self):
        image = load_icon(self.width, self.height, "resources/lever-mirror.png", "orange")
        self.set_sprite("orange", image)
        if self.door is not None:
            self.door.open()

    @HackableMethod
    def on_player_interaction(self, tick_data):
        self.release_tick = tick_data.tick + 50
        self.click()

    def on_tick(self, tick_data: TickData):
        if tick_data.tick == self.release_tick:
            self.unclick()


