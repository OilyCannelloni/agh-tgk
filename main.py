from dataclasses import dataclass, field

import pygame
from pygame_texteditor import TextEditor

from entities.blocks import WallSegment, WallBuilder
from entities.player import Player
from grid.grid import Grid
from grid.position import Position
from terminal.terminal import Terminal


@dataclass
class TickData:
    keys_down: list[int] = field(default_factory=list)

    def clear(self):
        pass


pygame.init()
screen = pygame.display.set_mode((2000,1500))
clock = pygame.time.Clock()


terminal = Terminal()

grid = Grid()
grid.place_existing_entity(Player(Position(100, 200)))
grid.place_existing_entity(WallSegment(Position(150, 150), Position(300, 150)))
grid.place_existing_entity(WallBuilder(Position(200, 450)))

tick_data = TickData()
while True:
    # Process player inputs.
    tick_data.clear()

    pygame_events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame_events:
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    if not terminal.enabled:
        tick_data.keys_down = pressed_keys
    else:
        tick_data.keys_down = []

    # Do logical updates here.
    # ...
    grid.process_dynamic_entities(**tick_data.__dict__)


    # Render the graphics here.
    # ...
    screen.fill("black")  # Fill the display with a solid color
    grid.sprites.update()
    grid.sprites.draw(screen)

    # displays editor functionality once per loop
    terminal.display_editor(pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed)
    terminal.on_tick()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(30)         # wait until next frame (at 30 FPS)




