"""Tests for game/ghost_ai.py."""

from game.ghost_ai import neighbors, next_step, run_away_step

# The 3x3 maze
#   (0,0) (1,0) (2,0)
#   (0,1) (1,1) (2,1)    <- (0,1) and (2,1) are dead ends
#   (0,2) (1,2) (2,2)
MAZE = [[9, 1, 3], [14, 10, 14], [13, 4, 7]]

# Same size, but the center (1,1) has walls on all sides, like a "42" cell
CLOSED_CENTER = [[9, 5, 3], [10, 15, 10], [12, 5, 6]]


def test_neighbors_open_sides() -> None:
    """Only the sides without a wall are neighbors."""
    assert neighbors(MAZE, (0, 0)) == [(1, 0), (0, 1)]


def test_neighbors_dead_end() -> None:
    """A dead end has only one neighbor."""
    assert neighbors(MAZE, (0, 1)) == [(0, 0)]


def test_next_step_first_cell_of_path() -> None:
    """The ghost takes the first cell of the shortest path."""
    assert next_step(MAZE, (0, 0), (2, 2)) == (1, 0)


def test_next_step_is_target_cell() -> None:
    """If the ghost is already on the target, it stays."""
    assert next_step(MAZE, (0, 0), (0, 0)) == (0, 0)


def test_next_step_no_path() -> None:
    """If the target cannot be reached, the ghost stays."""
    assert next_step(CLOSED_CENTER, (0, 0), (1, 1)) == (0, 0)


def test_run_away_never_toward_target() -> None:
    """A frightened ghost never takes the step toward the player."""
    for _ in range(20):
        assert run_away_step(MAZE, (1, 0), (2, 2)) != (1, 1)


def test_run_away_step_is_impossible() -> None:
    """In a dead end, a frightened ghost goes out toward the player."""
    assert run_away_step(MAZE, (0, 1), (2, 2)) == (0, 0)
