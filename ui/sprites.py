"""Load the sprite images from the assets folder."""

import sys
from pathlib import Path

import pygame

BASE_DIR = Path(getattr(sys, "_MEIPASS",
                        Path(__file__).resolve().parent.parent))
ASSETS_DIR = BASE_DIR / "assets"


SPRITE_FILES = {
    "player": "chataigne_left.png",
    "player_jump": "chataigne_jump_left.png",
    "red": "cat3.png",
    "pink": "cat1.png",
    "cyan": "cat2.png",
    "orange": "cat4.png",
    "pacgum": "pacgum.png",
    "super_pacgum": "carrot.png",
    "deco1": "fish.png",
    "deco2": "fish1.png"
}


def load_sprites() -> dict[str, pygame.Surface]:
    """Load every sprite listed in SPRITE_FILES.

    Must be called after pygame.display.set_mode(), because
    convert_alpha() needs the window to exist.

    Returns:
        A dict from sprite name to its image.
    """
    sprites = {}
    for name, filename in SPRITE_FILES.items():
        path = ASSETS_DIR / filename
        image = pygame.image.load(path).convert_alpha()
        sprites[name] = image

    return sprites
