import pygame
import pygamepal as pp
from entities.types import TickData

from levels.level import LevelTestDoor, LevelTeleporter, LevelLasers

from ui.hint_renderer import hint_renderer
from terminal.terminal import Terminal
from grid.grid import Grid
from utils import create_background

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
TILE_SIZE = 70

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

hint_renderer.initialize(screen)

pp_input = pp.Input()
terminal = Terminal(pp_input)

background_surface = create_background("resources/StoneFloorTexture.png", TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)

grid = Grid()

LevelTestDoor.load()


tick_data = TickData(0, pp_input)

while True:
    tick_data.tick += 1
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
        grid.process_player_input(tick_data)
        grid.process_dynamic_entities(tick_data)
    else:
        grid.process_dynamic_entities(TickData())


    # Render the graphics here.
    # ...
    screen.blit(background_surface, (0, 0))
    grid.sprites.update()
    grid.sprites.draw(screen)

    hint_renderer.render()

    # displays editor functionality once per loop
    terminal.display_terminal(pygame_events, pressed_keys)
    terminal.on_tick()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(30)  # wait until next frame (at 30 FPS)
