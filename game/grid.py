"""Grid helpers: wall directions and the shared wall check."""
N = 1
E = 2
S = 4
W = 8
ALL_WALLS = N | E | S | W

Position = tuple[int, int]

DIRECTIONS = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0),
}


def can_move(maze: list[list[int]], x: int, y: int, direction: int) -> bool:
    """Return True if there is no wall on this side of the cell.

    Args:
        maze: The maze grid, read as maze[y][x].
        x: Column of the cell.
        y: Row of the cell.
        direction: N, E, S or W.

    Returns:
        True if the cell has no wall in that direction.
    """
    return not (maze[y][x] & direction)
