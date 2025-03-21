import pygame
from pygame_texteditor import TextEditor

class Terminal(TextEditor):
    OFFSET_X = 1400
    OFFSET_Y = 200
    WIDTH = 500
    HEIGHT = 1000

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__(offset_x=1400, offset_y=200, editor_width=500, editor_height=1000,
                         screen=pygame.display.get_surface())
        self.set_line_numbers(True)
        self.set_syntax_highlighting(True)
        self.set_font_size(20)

    def on_tick(self):
        self.create_visual_effects()

    def create_visual_effects(self):
        pygame.draw.rect(pygame.display.get_surface(), pygame.color.Color("white"), (Terminal.OFFSET_X,
                         Terminal.OFFSET_Y, Terminal.WIDTH, Terminal.HEIGHT), width=5)