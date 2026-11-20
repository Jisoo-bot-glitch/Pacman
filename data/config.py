"""Read the game config: JSON with # comments, safe defaults"""

import json
import logging
import math
from dataclasses import dataclass, field
from typing import NamedTuple

logger = logging.getLogger(__name__)
MIN_LEVELS = 10


class Rule(NamedTuple):
    """To check one number of the config

    Attributes:
        kind: int or float, the type the game needs,
        default: when the key is missing or wrong,
        low: smallest allowed value,
        high: biggest allowed value, None means no limit
    """

    kind: type
    default: float
    low: float
    high: float | None


NUMBER_RULES: dict[str, Rule] = {
    'lives': Rule(int, 3, 1, 9),
    'points_per_pacgum': Rule(int, 10, 1, 1000),
    'points_per_super_pacgum': Rule(int, 50, 1, 1000),
    'points_per_ghost': Rule(int, 200, 1, 10000),
    'seed': Rule(int, 42, 1, None),
    'level_max_time': Rule(float, 90.0, 10.0, 600.0),
    'player_speed': Rule(float, 6.0, 1.0, 15.0),
    'ghost_speed': Rule(float, 5.0, 1.0, 15.0),
    'frightened_ghost_speed': Rule(float, 3.0, 0.5, 15.0),
    'frightened_time': Rule(float, 7.0, 1.0, 30.0),
    'ghost_respawn_time': Rule(float, 5.0, 1.0, 30.0),
}
LEVEL_RULES: dict[str, Rule] = {
    'width': Rule(int, 20, 15, 30),
    'height': Rule(int, 20, 11, 20),
}
DEFAULT_HIGHSCORE_FILE = 'highscores.json'


@dataclass(frozen=True)
class LevelConfig:
    """Size of the maze for one level

    Attributes:
        width: number of cells on x,
        height: number of cells on y
    """

    width: int = 20
    height: int = 20


def _default_levels() -> list[LevelConfig]:
    """Make the list of default levels

    Returns:
        10 levels with the default size
    """
    levels = []
    for _ in range(MIN_LEVELS):
        levels.append(LevelConfig())
    return levels


@dataclass(frozen=True)
class Config:
    """All the settings of the game, already checked

    Attributes:
        highscore_filename: file where the top 10 is saved,
        lives: from the start of the game,
        points_per_pacgum: for a small pacgum,
        points_per_super_pacgum: for a super-pacgum,
        points_per_ghost: for an edible ghost,
        seed: for the first level maze,
        level_max_time: to finish one level,
        player_speed: cells per second,
        ghost_speed: cells per second,
        frightened_ghost_speed: cells per second,
        frightened_time: seconds the ghosts stay edible,
        ghost_respawn_time: seconds before an eaten ghost comes back,
        levels: maze size of each level, at least 10.
    """

    highscore_filename: str = DEFAULT_HIGHSCORE_FILE
    lives: int = 3
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: float = 90.0
    player_speed: float = 6.0
    ghost_speed: float = 5.0
    frightened_ghost_speed: float = 3.0
    frightened_time: float = 7.0
    ghost_respawn_time: float = 5.0
    levels: list[LevelConfig] = field(default_factory=_default_levels)


def _strip_comments(text: str) -> str:
    """Replace every comment line with an empty line

    A comment line starts with #. The line is emptied and not removed,
    so JSON errors keep the right line number

    Args:
        text: raw content of the config file

    Returns:
        same text without the comment lines
    """
    lines = text.split('\n')
    clean = []
    for line in lines:
        if line.strip().startswith('#'):
            clean.append('')
        else:
            clean.append(line)
    return '\n'.join(clean)


def _check_number(key: str, raw: object, rule: Rule) -> float:
    """Check one number and return a safe value

    Wrong type - default, too small or too big - the limit.
    Each change is logged.

    Args:
        key: name of the key, used in the messages,
        raw: the value read from JSON, or None if the key is missing,
        rule: default and limits for this key

    Returns:
        a value the game can use. For int keys it is a real int.
    """
    if raw is None:
        logger.info('%s: missing, using %s', key, rule.default)
        return rule.default
    # bool must be checked first, because True is an int in Python
    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        logger.warning('%s: expected a number, got %r, using %s',
                       key, raw, rule.default)
        return rule.default
    value = float(raw)
    # json.loads accepts NaN and Infinity, the clamp would miss NaN
    if not math.isfinite(value):
        logger.warning('%s: got %r, using %s', key, raw, rule.default)
        return rule.default
    if rule.kind is int and not value.is_integer():
        logger.warning('%s: expected an integer, got %r, using %s',
                       key, raw, rule.default)
        return rule.default
    if value < rule.low:
        logger.warning('%s: %r is too small, using %s',
                       key, raw, rule.low)
        value = rule.low
    if rule.high is not None and value > rule.high:
        logger.warning('%s: %r is too big, using %s',
                       key, raw, rule.high)
        value = rule.high
    if rule.kind is int:
        return int(value)
    return value


def _check_filename(raw: object) -> str:
    """Check the highscore filename

    Args:
        raw: the value read from JSON, or None if the key is missing

    Returns:
        a non-empty filename
    """
    if raw is None:
        return DEFAULT_HIGHSCORE_FILE
    if not isinstance(raw, str) or raw.strip() == '':
        logger.warning('highscore_filename: expected a non-empty text, '
                       'got %r, using %s', raw, DEFAULT_HIGHSCORE_FILE)
        return DEFAULT_HIGHSCORE_FILE
    return raw.strip()


def _check_levels(raw: object) -> list[LevelConfig]:
    """Check the list of levels.

    A wrong level is replaced by a default one (not removed), so the
    level numbers stay the same. If there are less than 10 levels,
    default ones are added at the end.

    Args:
        raw: the value read from JSON, or None if the key is missing

    Returns:
        min 10 levels with a safe size
    """
    levels: list[LevelConfig] = []
    if raw is None:
        logger.info('levels: missing, using %d default levels',
                    MIN_LEVELS)
    elif not isinstance(raw, list):
        logger.warning('levels: expected a list, got %r, using %d '
                       'default levels', raw, MIN_LEVELS)
    else:
        number = 1
        for item in raw:
            if not isinstance(item, dict):
                logger.warning('level %d: expected an object, got %r, '
                               'using default size', number, item)
                levels.append(LevelConfig())
            else:
                size = {}
                for key, rule in LEVEL_RULES.items():
                    name = 'level ' + str(number) + ' ' + key
                    size[key] = int(_check_number(name, item.get(key),
                                                  rule))
                levels.append(LevelConfig(size['width'], size['height']))
            number += 1
        if len(raw) < MIN_LEVELS:
            logger.warning('levels: only %d, adding default levels up '
                           'to %d', len(raw), MIN_LEVELS)
    while len(levels) < MIN_LEVELS:
        levels.append(LevelConfig())
    return levels


def _read_json(path: str) -> dict[str, object] | None:
    """Read the file and parse it as JSON with comments

    Args:
        path: to the config file

    Returns:
        The parsed object, or None if the file can't be used
    """
    if not path.endswith('.json'):
        logger.error('%s: the config must be a .json file', path)
        return None
    try:
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
    except OSError as error:
        logger.error('%s: cannot read the file (%s)', path,
                     error.strerror)
        return None
    except UnicodeDecodeError:
        logger.error('%s: the file is not a text file', path)
        return None
    try:
        data = json.loads(_strip_comments(text))
    except json.JSONDecodeError as error:
        logger.error('%s: invalid JSON at line %d (%s)', path,
                     error.lineno, error.msg)
        return None
    if not isinstance(data, dict):
        logger.error('%s: the config must be a JSON object {...}', path)
        return None
    return data


def load_config(path: str) -> Config:
    """Load the config file and return safe settings. Never raises.

    If the file is missing or broken, all defaults are used. Unknown
    keys are ignored.

    Args:
        path: to the config file

    Returns:
        The checked settings
    """
    data = _read_json(path)
    if data is None:
        logger.warning('using the default config')
        return Config()
    known = list(NUMBER_RULES) + ['highscore_filename', 'levels']
    for key in data:
        if key not in known:
            logger.info('%s: unknown key, ignored', key)
    numbers = {}
    for key, rule in NUMBER_RULES.items():
        numbers[key] = _check_number(key, data.get(key), rule)
    return Config(
        highscore_filename=_check_filename(data.get('highscore_filename')),
        lives=int(numbers['lives']),
        points_per_pacgum=int(numbers['points_per_pacgum']),
        points_per_super_pacgum=int(numbers['points_per_super_pacgum']),
        points_per_ghost=int(numbers['points_per_ghost']),
        seed=int(numbers['seed']),
        level_max_time=numbers['level_max_time'],
        player_speed=numbers['player_speed'],
        ghost_speed=numbers['ghost_speed'],
        frightened_ghost_speed=numbers['frightened_ghost_speed'],
        frightened_time=numbers['frightened_time'],
        ghost_respawn_time=numbers['ghost_respawn_time'],
        levels=_check_levels(data.get('levels')),
    )
