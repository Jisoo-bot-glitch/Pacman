"""Draw the game screen: maze, pacgums, ghosts and the player."""

from typing import Protocol

import pygame

from game.ghost import Ghost, EATEN, FRIGHTENED
from game.grid import N, E, S, W, ALL_WALLS, Position


TILE_SIZE = 36
MARGIN = 20
HUD_HEIGHT = 48
BACKGROUND_COLOR = (255, 255, 255)
OUTSIDE_COLOR = (25, 35, 80)
WALL_COLOR = (139, 69, 19)
PATTERN_COLOR = (135, 206, 235)
WALL_WIDTH = 4
BLINK_MS = 250


class PlayerView(Protocol):
    """What draw() needs from the player."""

    @property
    def pos(self) -> Position:
        """Player cell as (x, y)."""
        ...


class GameView(Protocol):
    """What draw() needs from the game.

    Any object with these attributes can be drawn, so the Game class
    in game/game.py only has to provide them with these names.
    """

    @property
    def maze(self) -> list[list[int]]:
        """The maze grid, read as maze[y][x]."""
        ...

    @property
    def player(self) -> PlayerView:
        """The player (only its pos is used)."""
        ...

    @property
    def ghosts(self) -> list[Ghost]:
        """All ghosts of the level."""
        ...

    @property
    def pacgums(self) -> set[Position]:
        """Cells that still have a small pacgum."""
        ...

    @property
    def super_pacgums(self) -> set[Position]:
        """Cells that still have a super-pacgum."""
        ...


def cell_to_pixel(pos: Position) -> tuple[int, int]:
    """Return the top-left pixel of a maze cell.

    The maze starts below the HUD bar, with a margin around it.

    Args:
        pos: Cell position as (x, y).

    Returns:
        Pixel position (px, py) of the cell's top-left corner.
    """
    x, y = pos
    x = TILE_SIZE * x + MARGIN
    y = TILE_SIZE * y + MARGIN + HUD_HEIGHT

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
        sprites: All loaded images, from load_sprites().
    """
    count = 0
    fish1: Position | None = None
    fish2: Position | None = None
    for y, floor in enumerate(maze):
        for x, cell in enumerate(floor):
            px, py = cell_to_pixel((x, y))
            right = px + TILE_SIZE
            bottom = py + TILE_SIZE
            if cell & N:
                pygame.draw.line(screen,
                                 WALL_COLOR,
                                 (px, py),
                                 (right, py),
                                 WALL_WIDTH)
            if cell & E:
                pygame.draw.line(screen,
                                 WALL_COLOR,
                                 (right, py),
                                 (right, bottom),
                                 WALL_WIDTH)
            if cell & S:
                pygame.draw.line(screen,
                                 WALL_COLOR,
                                 (px, bottom),
                                 (right, bottom),
                                 WALL_WIDTH)
            if cell & W:
                pygame.draw.line(screen,
                                 WALL_COLOR,
                                 (px, py),
                                 (px, bottom),
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
    if fish1 is not None:
        screen.blit(sprites["deco1"], fish1)
    if fish2 is not None:
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
    Eaten ghosts are not drawn. Frightened ghosts are blue, and blink
    blue/white in their last seconds.

    Args:
        screen: The window surface to draw on.
        ghosts: All ghosts of the level.
        sprites: All loaded images, from load_sprites().
    """
    for ghost in ghosts:
        if ghost.state == EATEN:
            continue
        if ghost.state == FRIGHTENED:
            image = sprites["frightened"]
            white_turn = pygame.time.get_ticks() // BLINK_MS % 2 == 0
            if ghost.is_blinking and white_turn:
                image = sprites["frightened_end"]
        else:
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


def draw(screen: pygame.Surface, game: GameView,
         sprites: dict[str, pygame.Surface]) -> None:
    """Draw the whole game screen.

    Order: outside color, white maze area, maze, pacgums, ghosts, player.
    app.py calls this once per frame. It only reads game, never changes it.

    Args:
        screen: The window surface to draw on.
        game: Anything that matches GameView (the Game object).
        sprites: All loaded images, from load_sprites().
    """
    screen.fill(OUTSIDE_COLOR)
    maze_rect = (MARGIN, MARGIN + HUD_HEIGHT,
                 TILE_SIZE * len(game.maze[0]), TILE_SIZE * len(game.maze))
    pygame.draw.rect(screen, BACKGROUND_COLOR, maze_rect)
    draw_maze(screen, game.maze, sprites)
    draw_pacgums(screen, game.pacgums, game.super_pacgums, sprites)
    draw_ghosts(screen, game.ghosts, sprites)
    draw_player(screen, game.player.pos, sprites)
