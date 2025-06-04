import pygame


def tint_image(image: pygame.Surface, tint_color: str | tuple[int, int, int]) -> pygame.Surface:
    if isinstance(tint_color, str):
        rgb_color = pygame.Color(tint_color)
    else:
        rgb_color = pygame.Color(*tint_color)

    tinted = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            color = image.get_at((x, y))
            if color.a > 0:
                tinted.set_at((x, y), pygame.Color(rgb_color.r, rgb_color.g, rgb_color.b, color.a))

    return tinted

def load_icon(width, height, path, color=None):
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        raise FileNotFoundError(f"Failed to load image from '{path}': {e}")

    image = pygame.transform.scale(image, (width, height))

    if color:
        image = tint_image(image, color)

    return image

def create_surface(width, height, tile_path, tile_size=10, color=None):
    try:
        tile_icon = load_icon(tile_size, tile_size, tile_path, color)
    except FileNotFoundError:
        return None

    if tile_icon is None:
        return None

    tiles_x = width // tile_size
    tiles_y = height // tile_size

    surface = pygame.Surface((width, height))

    for x in range(tiles_x):
        for y in range(tiles_y):
            surface.blit(tile_icon, (x * tile_size, y * tile_size))

    return surface

def create_background(tile_path, tile_size, screen_width, screen_height):
    try:
        background_tile = load_icon(tile_size, tile_size, tile_path)
    except pygame.error as e:
        raise FileNotFoundError(f"Failed to load background from '{tile_path}': {e}")

    background_surface = pygame.Surface((screen_width, screen_height))
    for x in range(0, screen_width, tile_size):
        for y in range(0, screen_height, tile_size):
            background_surface.blit(background_tile, (x, y))

    return background_surface