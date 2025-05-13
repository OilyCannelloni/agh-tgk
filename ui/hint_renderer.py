import pygame

from entities.types import EntityType
from grid.grid import Grid

grid = Grid()


class GameHintRenderer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._screen = None
        self._font = None
        self._hint_rect = None
        self._hint_surface = None
        self._interaction_hints = [(EntityType.INTERACTABLE, "E", "USE"), (EntityType.HACKABLE, "T", "HACK")]

    def initialize(self, screen):
        if not self._font:
            pygame.font.init()
            self._font = pygame.font.Font(None, 24)
        self._screen = screen

    def _create_hint_surface(self, key, text):
        key_bg_width, key_bg_height = 40, 40
        key_background = pygame.Surface((key_bg_width, key_bg_height), pygame.SRCALPHA)
        pygame.draw.rect(key_background, (100, 100, 100), key_background.get_rect(), 2)

        key_surface = self._font.render(key.upper(), True, (200, 200, 200))
        key_rect = key_surface.get_rect(center=(key_bg_width // 2, key_bg_height // 2))
        key_background.blit(key_surface, key_rect)

        text_surface = self._font.render(text.upper(), True, (200, 200, 200))
        text_rect = text_surface.get_rect(left=key_bg_width + 10, centery=key_bg_height // 2)

        total_width = key_bg_width + 60 + text_rect.width
        total_height = key_bg_height
        combined_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        combined_surface.blit(key_background, (0, 0))
        combined_surface.blit(text_surface, text_rect.topleft)

        return combined_surface

    def show_hint(self, owner_type: EntityType):
        if not self._screen:
            raise RuntimeError("GameHintRenderer not initialized. Call initialize(screen) first.")

        if self._hint_surface is not None and self._hint_rect is not None:
            return

        hint_surfaces = []
        for req_e_type, key, text in self._interaction_hints:
            print(req_e_type)
            if req_e_type in owner_type:
                hint_surfaces.append(self._create_hint_surface(key, text))

        total_width = sum(surface.get_width() for surface in hint_surfaces) + 10 * (len(hint_surfaces) - 1)
        max_height = max(surface.get_height() for surface in hint_surfaces)
        background = pygame.Surface((total_width, max_height), pygame.SRCALPHA)

        x_offset = 0
        for surface in hint_surfaces:
            background.blit(surface, (x_offset, 0))
            x_offset += surface.get_width() + 60

        screen_width, screen_height = self._screen.get_size()
        self._hint_rect = background.get_rect(
            centerx=screen_width // 2,
            bottom=screen_height - 50
        )
        self._hint_surface = background

    def clear_hint(self):
        self._hint_surface = None
        self._hint_rect = None
        grid.current_interactable_entity = None


    def render(self):
        if not self._screen:
            raise RuntimeError("GameHintRenderer not initialized. Call initialize(screen) first.")

        if self._hint_surface and self._hint_rect:
            self._screen.blit(self._hint_surface, self._hint_rect)


hint_renderer = GameHintRenderer()
