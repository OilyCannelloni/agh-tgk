import pygame
from pygame_texteditor import TextEditor

class Terminal(TextEditor):
    OFFSET_X = 1200
    OFFSET_Y = 200
    WIDTH = 700
    HEIGHT = 1000
    BORDER_WIDTH = 5

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__(offset_x=Terminal.OFFSET_X, offset_y=Terminal.OFFSET_Y,
                         editor_width=Terminal.WIDTH, editor_height=Terminal.HEIGHT,
                         screen=pygame.display.get_surface())

        pygame.key.set_repeat(0, 0)
        self.set_syntax_highlighting(True)
        self.set_font_size(20)
        self.set_drag_end_after_last_line()
        self.set_line_numbers(True)
        self.enabled = False
        self.rect = pygame.rect.Rect(Terminal.OFFSET_X - Terminal.BORDER_WIDTH,
                                     Terminal.OFFSET_Y - Terminal.BORDER_WIDTH, Terminal.WIDTH, Terminal.HEIGHT)
        self.line_start_y += 5
        self.initialize()


    def on_tick(self):
        self.create_visual_effects()

    def create_visual_effects(self):
        self.set_line_numbers(True)
        pygame.draw.rect(pygame.display.get_surface(), pygame.color.Color("white"), self.rect, width=5)

    def set_enabled(self, enable: bool):
        self.enabled = enable
        if enable:
            self.color_coding_background = (40, 40, 40)
        else:
            self.color_coding_background = (70, 70, 70)


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

    def set_text_raw(self, ss: str):
        ss = ss.split("\n")
        if all([line.startswith("    ") or len(line) == 0 for line in ss]):
            for i in range(len(ss)):
                ss[i] = ss[i].removeprefix("    ")

        self.set_text_from_list(ss)

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

    def display_editor(self, pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed):
        """Display the editor.

        The function should be called once within every pygame loop.

        :param pygame_events:
        :param pressed_keys:
        :param mouse_x:
        :param mouse_y:
        :param mouse_pressed:
        """

        if mouse_pressed[0]:
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.set_enabled(True)
            else:
                self.set_enabled(False)

        # RENDERING 1 - Background objects
        self.render_background_coloring()
        self.render_line_numbers()

        # RENDERING 2 - Line contents, caret
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

        if not self.enabled:
            return

        self.cycleCounter = self.cycleCounter + 1
        self.handle_keyboard_input(pygame_events, pressed_keys)
        self.handle_mouse_input(pygame_events, mouse_x, mouse_y, mouse_pressed)
        self.update_line_number_display()

