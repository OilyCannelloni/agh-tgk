import pygame
import pygamepal as pp

from entities.blocks import WallSegment, ExampleInteractable
from entities.player import Player
from entities.types import TickData

from grid.position import Position
from ui.hint_renderer import hint_renderer
from terminal.terminal import Terminal
from grid.grid import Grid

pygame.init()
screen = pygame.display.set_mode((2000,1200))
clock = pygame.time.Clock()

hint_renderer.initialize(screen)

grid = Grid()
grid.place_existing_entity(Player(Position(100, 200)))
grid.place_existing_entity(WallSegment(Position(150, 150), Position(400, 150)))
grid.place_existing_entity(ExampleInteractable(Position(200, 200)))

pp_input = pp.Input()
terminal = Terminal(pp_input)

tick_data = TickData(pp_input)
while True:
    # Process player inputs.
    pygame_events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()

    for event in pygame_events:
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Do logical updates here.
    # ...
    if not terminal.is_enabled():
        grid.process_player_input(tick_data.pp_input)
        grid.process_dynamic_entities(tick_data)
    else:
        grid.process_dynamic_entities(TickData())


    # Render the graphics here.
    # ...
    screen.fill("black")  # Fill the display with a solid color
    grid.sprites.update()
    grid.sprites.draw(screen)

    hint_renderer.render()

    # displays editor functionality once per loop
    terminal.display_terminal(pygame_events, pressed_keys)
    terminal.on_tick()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(30)  # wait until next frame (at 30 FPS)
