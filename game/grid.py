"""Grid helpers: wall directions and the shared wall check."""
N = 1
E = 2
S = 4
W = 8


def can_move(maze: list[list[int]], x: int, y: int, direction: int) -> bool:
    """Return True if there is no wall on this side of the cell."""
    return not (maze[y][x] & direction)
