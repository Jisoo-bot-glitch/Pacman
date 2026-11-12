"""Interpretation action from keyboard"""

from enum import Enum, auto


class Action(Enum):
    """ """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    PAUSE = auto()
    CHEAT_INVINCIBLE = auto()
    CHEAT_SKIP_LEVEL = auto()
    CHEAT_FREEZE = auto()
    CHEAT_LIFE_EXTRA = auto()
    CHEAT_SPEED = auto()
