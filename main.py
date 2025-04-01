from dataclasses import dataclass, field

import pygame

from entities.blocks import WallSegment, ExampleInteractable
from entities.player import Player
from grid.grid import Grid
from grid.position import Position
from ui.hint_renderer import hint_renderer


@dataclass
class TickData:
    keys_down: list[int] = field(default_factory=list)

    def clear(self):
        pass


pygame.init()
screen = pygame.display.set_mode((1280,720))
hint_renderer.initialize(screen)
clock = pygame.time.Clock()

grid = Grid()
grid.place_entity(Player(Position(100, 200)))
grid.place_entity(WallSegment(Position(150, 150), Position(400, 150)))
grid.place_entity(ExampleInteractable(Position(200, 200)))

tick_data = TickData()
while True:
    # Process player inputs.
    tick_data.clear()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            tick_data.keys_down.append(event.key)

        if event.type == pygame.KEYUP:
            tick_data.keys_down.remove(event.key)

    # Do logical updates here.
    # ...
    grid.process_dynamic_entities(**tick_data.__dict__)
    grid.process_player_input(tick_data.keys_down)

    # Render the graphics here.
    # ...
    screen.fill("black")  # Fill the display with a solid color
    grid.sprites.update()
    grid.sprites.draw(screen)

    hint_renderer.render()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(30)  # wait until next frame (at 30 FPS)
