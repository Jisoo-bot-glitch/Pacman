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


def test_speed_zero_does_not_move() -> None:
    """At speed 0, the ghost does not move."""
    ghost = Ghost("red", (0, 0), speed=0)
    ghost.update(MAZE, TARGET, 1)
    assert ghost.pos == (0, 0)
    assert ghost._move_timer == 0.0


def test_direction_follows_the_move() -> None:
    """The ghost;s direction follows the move."""
    ghost = Ghost("red", (0, 0), speed=5.0)
    ghost.update(MAZE, TARGET, 0.25)
    assert ghost.pos == (1, 0)
    assert ghost.direction == E
    ghost.update(MAZE, TARGET, 0.25)
    assert ghost.pos == (1, 1)
    assert ghost.direction == S


def test_frighten_sets_state_and_timer() -> None:
    """Calling frighten() sets FRIGHTENED and fills the timer."""
    ghost = Ghost("red", (0, 0), frightened_time=8.0)
    ghost.frighten()
    assert ghost.state == FRIGHTENED
    assert ghost.state_timer == 8.0


def test_chase_ghost_cannot_be_eaten() -> None:
    """A ghost in CHASE cannot be eaten."""
    ghost = Ghost("red", (0, 0))
    ghost.get_eaten()
    assert ghost.state == CHASE


def test_state_change_from_frighten_to_chase() -> None:
    """After FRIGHTENED time, the ghost goes back to CHASE."""
    ghost = Ghost("red", (0, 0))
    ghost.frighten()
    ghost.update(MAZE, TARGET, 7.5)
    assert ghost.state == CHASE
    assert ghost.state_timer == 0.0


def test_back_to_spawn() -> None:
    """After being eaten, the ghost goes back to its spawn.

    speed=0 so it does not move away in the same update.
    """
    ghost = Ghost("red", (0, 0), speed=0)
    ghost.pos = (0, 1)
    ghost.frighten()
    ghost.get_eaten()
    assert ghost.state == EATEN
    ghost.update(MAZE, TARGET, 5.5)
    assert ghost.state == CHASE
    assert ghost.pos == ghost.spawn


def test_is_blinking() -> None:
    """The ghost starts blinking when 2 seconds of FRIGHTENED are left."""
    ghost = Ghost("red", (0, 0))
    ghost.frighten()
    assert not ghost.is_blinking
    ghost.update(MAZE, TARGET, 5.5)
    assert ghost.is_blinking
