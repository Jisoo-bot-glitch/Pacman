""" """
Position = tuple[int, int]
NO_DIRECTION = 0


class Player:
    """ """
    def __init__(self, start: Position, speed: float = 6.0) -> None:
        """Create ...
        Args:
        """
        self.start: Position = start
        self.pos: Position = start
        self.direction: int = NO_DIRECTION
        self.next_direction: int = NO_DIRECTION
        self.speed: float = speed
        self._move_timer: float = 0.0

    def set_direction(self, direction: int) -> None:
        """Create ...
        Args:
        """
        self.next_direction = direction

    def update(self, maze: list[list[int]], dt: float) -> None:
        """Create ...
        Args:
        """
        ...

    def reswap(self) -> None:
        """Create ...
        Args:
        """
        self.pos = self.start
        self.direction = NO_DIRECTION
        self.next_direction = NO_DIRECTION
        self._move_timer = 0.0
