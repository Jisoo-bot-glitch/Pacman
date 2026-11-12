""" """

from dataclasses import dataclass


@dataclass
class Session:
    """Attributes"""
    score: int = 0
    lives: int = 3
    level: int = 1
    time_left: float = 90.0

    def add_score(self, points: int) -> None:
        """Create ...
        Args:
        """
        if points > 0:
            self.score += points

    def lose_life(self) -> None:
        """Create ...
        Args:
        """
        self.lives = max(0, self.lives - 1)

    def is_game_over(self) -> bool:
        """Create ...
        Args:
        """
        return self.lives == 0
