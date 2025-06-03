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

def load_icon(width, height, path, color):
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        raise FileNotFoundError(f"Failed to load image from '{path}': {e}")

    image = pygame.transform.scale(image, (width, height))
    return tint_image(image, color)