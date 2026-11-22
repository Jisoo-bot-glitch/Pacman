"""Tests for game/grid.py."""

from game.grid import can_move, N, E, S, W, DIRECTIONS

# The 3x3 maze
#   (0,0) (1,0) (2,0)
#   (0,1) (1,1) (2,1)    <- (0,1) and (2,1) are dead ends
#   (0,2) (1,2) (2,2)
MAZE = [[9, 1, 3], [14, 10, 14], [13, 4, 7]]

# Same size, but the center (1,1) has walls on all sides, like a "42" cell
CLOSED_CENTER = [[9, 5, 3], [10, 15, 10], [12, 5, 6]]


def test_wall_cell() -> None:
    """A side with a wall is blocked."""
    assert not can_move(MAZE, 0, 0, N)


def test_no_wall_cell() -> None:
    """A side without a wall is open."""
    assert can_move(MAZE, 0, 0, E)


def test_all_wall() -> None:
    """A "42" cell has a wall on every side."""
    for direction in (N, E, S, W):
        assert not can_move(CLOSED_CENTER, 1, 1, direction)


def test_order_of_directions() -> None:
    """DIRECTIONS is in N, E, S, W order, check in that order."""
    assert list(DIRECTIONS) == [N, E, S, W]
