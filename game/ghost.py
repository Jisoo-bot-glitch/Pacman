"""Ghost data and state changes."""

from game.grid import E, N, S, W, Position
from game.ghost_ai import next_step

CHASE = "chase"
FRIGHTENED = "frightened"
EATEN = "eaten"


class Ghost:
    """One ghost: where it is, where it goes, and its state."""

    def __init__(self, name: str,
                 pos: Position,
                 speed: float = 5.0) -> None:
        """Create a ghost at its spawn corner, chasing.

        Args:
            name: Ghost name ("red", "pink", "cyan" or "orange").
            pos: Spawn cell as (x, y).
            speed: Cells per second.
        """
        self.name = name
        self.pos = pos
        self.spawn = pos
        self.direction = W
        self.state = CHASE
        self.speed = speed
        self._move_timer = 0.0

    def update(self, maze: list[list[int]], target: Position,
               dt: float) -> None:
        """Move one cell toward target when enough time has passed.

        Time is collected in _move_timer. Each time it reaches one step
        (1 / speed seconds), the ghost moves one cell and that step is
        taken out of the timer, so the leftover time is kept.
        A speed of 0 or less means the ghost does not move.
        After moving, direction is set to the way the ghost went.
        If it did not move, direction stays the same.

        Args:
            maze: The maze grid, read as maze[y][x].
            target: The cell to move toward.
            dt: Seconds since the last frame.
        """
        if self.speed <= 0:
            return
        self._move_timer += dt
        step_time = 1 / self.speed
        if self._move_timer >= step_time:
            self._move_timer -= step_time
            old_x, old_y = self.pos
            self.pos = next_step(maze, self.pos, target)
            new_x, new_y = self.pos
            if new_x > old_x:
                self.direction = E
            elif new_x < old_x:
                self.direction = W
            elif new_y > old_y:
                self.direction = S
            elif new_y < old_y:
                self.direction = N
