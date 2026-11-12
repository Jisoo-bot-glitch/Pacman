"""Ghost data and state changes."""

from game.grid import W

CHASE = "chase"
FRIGHTENED = "frightened"
EATEN = "eaten"


class Ghost:
    """One ghost: where it is, where it goes, and its state."""

    def __init__(self, name: str, pos: tuple[int, int]) -> None:
        """Create a ghost at its spawn corner, chasing."""
        self.name = name
        self.pos = pos
        self.spawn = pos
        self.direction = W
        self.state = CHASE
