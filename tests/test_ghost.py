"""Tests for game/ghost.py."""

from game.ghost import CHASE, EATEN, FRIGHTENED, Ghost
from game.grid import E, S

# Same 3x3 maze as in test_ghost_ai.py.
# Shortest path from (0,0) to (2,2): (1,0) -> (1,1) -> (1,2) -> (2,2)
MAZE = [[9, 1, 3], [14, 10, 14], [13, 4, 7]]
TARGET = (2, 2)


def test_moves_one_cell_after_one_step_time() -> None:
    """At 5 cells/s, the ghost waits 0.2 s, then moves one cell."""
    ghost = Ghost("red", (0, 0), speed=5.0)
    ghost.update(MAZE, TARGET, 0.1)
    assert ghost.pos == (0, 0)
    ghost.update(MAZE, TARGET, 0.15)
    assert ghost.pos == (1, 0)
