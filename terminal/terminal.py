import dataclasses
from typing import TYPE_CHECKING

import pygame
from pygame.key import ScancodeWrapper
from pygame_texteditor import TextEditor
import pygamepal as pp

if TYPE_CHECKING:
    from entities.base import HackableEntity

@dataclasses.dataclass
class LineTypeInterval:
    start: int
    end: int
    editable: bool


class Terminal(TextEditor):
    OFFSET_X = 720
    OFFSET_Y = 120
    WIDTH = 420
    HEIGHT = 480
    BORDER_WIDTH = 5

    _instance = None
    initialized = False
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, input: pp.Input = None):
        if Terminal.initialized:
            return
        super().__init__(offset_x=Terminal.OFFSET_X, offset_y=Terminal.OFFSET_Y,
                         editor_width=Terminal.WIDTH, editor_height=Terminal.HEIGHT,
                         screen=pygame.display.get_surface())

        pygame.key.set_repeat(0, 0)
        self.set_syntax_highlighting(True)
        self.set_font_size(14)
        self.set_drag_end_after_last_line()
        self.set_line_numbers(True)
        self.enabled = False
        self.active_entity: HackableEntity = None
        self.rect = pygame.rect.Rect(Terminal.OFFSET_X - Terminal.BORDER_WIDTH,
                                     Terminal.OFFSET_Y - Terminal.BORDER_WIDTH,
                                     Terminal.WIDTH + 2 * Terminal.BORDER_WIDTH,
                                     Terminal.HEIGHT + 2 * Terminal.BORDER_WIDTH)
        self.line_start_y += 5
        self.initialize()
        self.input: pp.Input = input

        button_width = 100
        button_height = 50
        self.button = pp.Button(
            input=self.input,
            position=(Terminal.OFFSET_X + (Terminal.WIDTH + Terminal.BORDER_WIDTH - button_width) // 2,
                      Terminal.OFFSET_Y + Terminal.HEIGHT + Terminal.BORDER_WIDTH + 20),
            size=(button_width, button_height),
            text="Run code",
            onSelected=self.apply_code,
            foregroundColor=(200, 200, 200),
            backgroundColor=(60, 60, 60)
        )

        self.num_read_only_lines = 0

        Terminal.initialized = True


    def on_tick(self):
        self.create_visual_effects()

    def create_visual_effects(self):
        self.set_line_numbers(True)
        pygame.draw.rect(pygame.display.get_surface(), pygame.color.Color("gray9"), self.rect, width=5)

    def apply_code(self, button):
        self.active_entity.apply_code(self.get_text_as_string())

    def set_active_entity(self, entity: "HackableEntity"):
        self.active_entity = entity

    def set_enabled(self, enable: bool):
        self.enabled = enable
        if enable:
            self.color_coding_background = (40, 40, 40)
        else:
            self.color_coding_background = (70, 70, 70)

    def is_enabled(self):
        return self.enabled


    def initialize(self):
        pygame.draw.rect(
            self.screen,
            self.color_coding_background,
            (
                self.editor_offset_x,
                self.editor_offset_y,
                self.editor_width,
                self.editor_height,
            ),
        )

    def clear(self):
        self.num_read_only_lines = 0
        self.editor_lines = []
        self.active_entity = None

    def set_read_only_code(self, code_str: str):
        lines = self._format_code(code_str)
        self.editor_lines = lines
        self.num_read_only_lines = len(lines)

    def set_hackable_code(self, code_str: str):
        lines = self._format_code(code_str)
        self.editor_lines.append("")
        self.editor_lines.extend(lines)

    def _format_code(self, code: str):
        lines = code.split("\n")
        if all([line.startswith("    ") or len(line) == 0 for line in lines]):
            for i in range(len(lines)):
                lines[i] = lines[i].removeprefix("    ")
        return lines

    def update_caret_position(self) -> None:
        """Update the caret position based on current position by line and letter indices.
        We add one pixel to the x coordinate so the caret is fully visible if it is at the start of the line.
        """
        self.caret_x = (
                self.line_start_x + (self.chosen_letter_index * self.letter_width) + 1
        )
        self.caret_y = self.line_start_y - 5 + (
                (self.chosen_line_index - self.first_showable_line_index)
                * self.line_height_including_margin
        )

    def render_line_contents(self, line_contents):
        super().render_line_contents(line_contents)

        if self.num_read_only_lines <= 0:
            return

        surf = pygame.Surface((
            self.editor_width,
            self.line_height_including_margin * self.num_read_only_lines))

        surf.fill(pygame.Color(150, 0, 0))
        surf.set_alpha(40)
        self.screen.blit(surf, (self.line_start_x, self.line_start_y))

    def display_terminal(self, pygame_events, pressed_keys: ScancodeWrapper):
        """Display the editor.
        The function should be called once within every pygame loop.
        """
        self.input.update()
        self.button.update()

        if self.input.isMouseButtonPressed(0):
            if self.rect.collidepoint(self.input.currentMousePosition[0], self.input.currentMousePosition[1]):
                self.set_enabled(True)
            else:
                self.set_enabled(False)

        # RENDERING 1 - Background objects
        self.render_background_coloring()
        self.button.draw(self.screen)

        # RENDERING 2 - Line contents, caret
        mouse_x, mouse_y = self.input.currentMousePosition
        mouse_pressed = self.input.currentMouseButtonStates
        self.render_highlight(mouse_x, mouse_y)
        if self.syntax_highlighting_python:
            # syntax highlighting for code
            line_contents = self.get_syntax_coloring_dicts()
        else:
            # single-color text
            line_contents = self.get_single_color_dicts()
        self.render_line_contents(line_contents)
        self.render_caret()

        # RENDERING 3 - scrollbar
        self.render_scrollbar_vertical()
        self.clock.tick(self.FPS)
        self.render_line_numbers()
        self.update_line_number_display()
        self.cycleCounter = self.cycleCounter + 1

        if not self.enabled:
            return

        self.handle_mouse_input(pygame_events, mouse_x, mouse_y, mouse_pressed)

        # what a dirty hack byt hey - it works at least
        if not pressed_keys[pygame.K_LCTRL] and not pressed_keys[pygame.K_RCTRL]:
            if self.caret_y < self.num_read_only_lines * self.line_height_including_margin + self.line_start_y:
                i = 0
                while i < len(pygame_events):
                    if pygame_events[i].type == pygame.KEYDOWN and len(pygame.key.name(pygame_events[i].key)) == 1:
                        pygame_events.pop(i)
                    else:
                        i += 1

        self.handle_keyboard_input(pygame_events, pressed_keys)



