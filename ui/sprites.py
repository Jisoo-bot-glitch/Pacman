"""Load the sprite images from the assets folder."""

import sys
from pathlib import Path
import pygame

from ui.game_view import TILE_SIZE

BASE_DIR = Path(getattr(sys, "_MEIPASS",
                        Path(__file__).resolve().parent.parent))
ASSETS_DIR = BASE_DIR / "assets"

SPRITE_FILES = {
    "player": "chataigne_left.png",
    "player_jump": "chataigne_jump_left.png",
    "red": "cat1.png",
    "pink": "cat2.png",
    "cyan": "cat3.png",
    "orange": "cat4.png",
    "pacgum": "pacgum.png",
    "super_pacgum": "carrot.png",
    "deco1": "fish.png",
    "deco2": "fish1.png",
    "frightened": "cat_blue.png",
    "frightened_end": "cat_white.png",
}


def load_sprites() -> dict[str, pygame.Surface]:
    """Load every sprite listed in SPRITE_FILES.

    Must be called after pygame.display.set_mode(), because
    convert_alpha() needs the window to exist.
    If an image cannot be loaded, a colored square is used instead
    and a warning is printed, so the game does not crash.

    Returns:
        A dict from sprite name to its image.
    """
    sprites = {}
    for name, filename in SPRITE_FILES.items():
        path = ASSETS_DIR / filename
        try:
            image = pygame.image.load(path).convert_alpha()
        except (FileNotFoundError, pygame.error) as err:
            print(f"Warning: cannot load {path}: {err}", file=sys.stderr)
            image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            image.fill((255, 20, 147))
        sprites[name] = image

    return sprites
