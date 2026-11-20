"""Ghost data and state changes."""

from game.grid import E, N, S, W, Position
from game.ghost_ai import next_step

CHASE = "chase"
FRIGHTENED = "frightened"
EATEN = "eaten"
BLINK_TIME = 2.0


class Ghost:
    """One ghost: where it is, where it goes, and its state."""

    def __init__(self, name: str,
                 pos: Position,
                 speed: float = 5.0,
                 frightened_speed: float = 3.0,
                 frightened_time: float = 7.0,
                 respawn_time: float = 5.0) -> None:
        """Create a ghost at its spawn corner, chasing.

        Args:
            name: Ghost name ("red", "pink", "cyan" or "orange").
            pos: Spawn cell as (x, y).
            speed: Cells per second when chasing.
            frightened_speed: Cells per second when frightened.
            frightened_time: Seconds a ghost stays frightened.
            respawn_time: Seconds before an eaten ghost comes back.
        """
        self.name = name
        self.pos = pos
        self.spawn = pos
        self.direction = W
        self.state = CHASE
        self.speed = speed
        self.frightened_speed = frightened_speed
        self.frightened_time = frightened_time
        self.respawn_time = respawn_time
        self.state_timer = 0.0
        self._move_timer = 0.0

    @property
    def is_blinking(self) -> bool:
        """True in the last BLINK_TIME seconds of being frightened.

        game_view uses it to switch between the blue and white sprite.
        """
        return self.state == FRIGHTENED and self.state_timer <= BLINK_TIME

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

    def frighten(self) -> None:
        """Make the ghost frightened (the player ate a super-pacgum).

        The timer starts again from frightened_time, even if the ghost
        was already frightened. An eaten ghost is not affected.
        """
        if self.state == EATEN:
            return
        self.state = FRIGHTENED
        self.state_timer = self.frightened_time

    def get_eaten(self) -> None:
        """Send a frightened ghost home (the player ate it).

        Only a frightened ghost can be eaten. It disappears for
        respawn_time seconds, then comes back at its spawn corner.
        """
        if self.state != FRIGHTENED:
            return
        self.state = EATEN
        self.state_timer = self.respawn_time
