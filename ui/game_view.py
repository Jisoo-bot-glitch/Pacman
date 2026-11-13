"""Draw the game screen: maze, pacgums, ghosts and the player."""

import pygame

from game.ghost import Ghost
from game.grid import N, E, S, W, ALL_WALLS

Position = tuple[int, int]

TILE_SIZE = 36
MARGIN = 20
HUD_HEIGHT = 48

BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (139, 69, 19)
PATTERN_COLOR = (135, 206, 235)
WALL_WIDTH = 4


def cell_to_pixel(pos: Position) -> tuple[int, int]:
    """Return the top-left pixel of a maze cell.

    Args:
        pos: Cell position as (x, y).

    Returns:
        Pixel position (px, py) of the cell's top-left corner.
    """
    x, y = pos
    x = TILE_SIZE * x + MARGIN
    y = TILE_SIZE * y + MARGIN

    return x, y


def window_size(maze: list[list[int]]) -> tuple[int, int]:
    """Return the window size needed to show this maze and the HUD.

    Args:
        maze: The maze grid, read as maze[y][x].

    Returns:
        Window size (width, height) in pixels.
    """
    height = TILE_SIZE * len(maze) + MARGIN * 2 + HUD_HEIGHT
    width = TILE_SIZE * len(maze[0]) + MARGIN * 2

    return width, height


def draw_maze(screen: pygame.Surface, maze: list[list[int]],
              sprites: dict[str, pygame.Surface]) -> None:
    """Draw the "42" cells and every wall of the maze.

    Args:
        screen: The window surface to draw on.
        maze: The maze grid, read as maze[y][x].
    """
    count = 0
    fish1 = (0, 0)
    fish2 = (0, 0)
    for y, floor in enumerate(maze):
        for x, cell in enumerate(floor):
            px, py = cell_to_pixel((x, y))
            right = px + TILE_SIZE, py + TILE_SIZE
            bottom = px + TILE_SIZE, py + TILE_SIZE
            if cell & N:
                pygame.draw.line(screen,
                                 WALL_COLOR,
                                 (px, py),
                                 (px + TILE_SIZE, py),
                                 WALL_WIDTH)
            if cell & E:
                pygame.draw.line(screen,
                                 WALL_COLOR,
                                 (px + TILE_SIZE, py),
                                 (right),
                                 WALL_WIDTH)
            if cell & S:
                pygame.draw.line(screen,
                                 WALL_COLOR,
                                 (px, py + TILE_SIZE),
                                 (bottom),
                                 WALL_WIDTH)
            if cell & W:
                pygame.draw.line(screen,
                                 WALL_COLOR,
                                 (px, py),
                                 (px, py + TILE_SIZE),
                                 WALL_WIDTH)
            if cell == ALL_WALLS:
                pygame.draw.rect(screen,
                                 PATTERN_COLOR,
                                 (px, py, TILE_SIZE, TILE_SIZE))
                count += 1
                if count == 5:
                    fish1 = (px, py)
                if count == 11:
                    fish2 = (px, py)
        screen.blit(sprites["deco1"], fish1)
        screen.blit(sprites["deco2"], fish2)


def draw_pacgums(screen: pygame.Surface, pacgums: set[Position],
                 super_pacgums: set[Position],
                 sprites: dict[str, pygame.Surface]) -> None:
    """Draw the pacgums and super-pacgums that are still in the maze.

    Only draws what is in the sets. It never removes anything:
    eating is decided by the game rules.

    Args:
        screen: The window surface to draw on.
        pacgums: Cells that still have a small pacgum.
        super_pacgums: Cells that still have a super-pacgum.
        sprites: All loaded images, from load_sprites().
    """
    for leaf in pacgums:
        image = sprites["pacgum"]
        x, y = cell_to_pixel(leaf)
        screen.blit(image, (x, y))
    for carrot in super_pacgums:
        image = sprites["super_pacgum"]
        x, y = cell_to_pixel(carrot)
        screen.blit(image, (x, y))


def draw_ghosts(screen: pygame.Surface, ghosts: list[Ghost],
                sprites: dict[str, pygame.Surface]) -> None:
    """Draw every ghost on its cell.

    Args:
        screen: The window surface to draw on.
        ghosts: All ghosts of the level.
        sprites: All loaded images, from load_sprites().
    """
    for ghost in ghosts:
        image = sprites[ghost.name]
        x, y = cell_to_pixel(ghost.pos)
        screen.blit(image, (x, y))


def draw_player(screen: pygame.Surface, pos: Position,
                sprites: dict[str, pygame.Surface]) -> None:
    """Draw the player on its cell.

    Args:
        screen: The window surface to draw on.
        pos: Player cell as (x, y).
        sprites: All loaded images, from load_sprites().
    """
    player = sprites["player"]
    x, y = cell_to_pixel(pos)
    screen.blit(player, (x, y))
