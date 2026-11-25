*This activity has been created as part of the 42 curriculum by jisobaek, efatin.*

# Pac-Man (rabbit edition)

## Description

A Pac-Man game in Python with pygame-ce. You are a rabbit in a maze.
Eat all the leaves to finish the level, and avoid the cats.
Eat a carrot to frighten the cats for a few seconds: they turn blue, run away, and you can eat them.

- 10 levels. The first maze is always the same (seed 42), the next ones are random.
- Mazes come from the assigned A-Maze-ing package (`mazegenerator`).
- Everything (lives, points, speeds, times, maze sizes) is set in a JSON config file.
- Top 10 high scores, saved in a file.
- Cheat keys for the evaluation.
- All sprites are our own, drawn by hand.

The goal of the activity is to build a full game in a team of two:
game logic, ghost AI, drawing, config, tests, packaging, and project management.

## Instructions

### Play the packaged game (no Python needed)

Download the game from itch.io, unzip it, open a terminal in the folder and run:

```bash
./pac-man config.json
```

The game needs exactly one argument: a JSON config file.
`INSTRUCTIONS.txt` in the package explains the controls and rules.

### Run from the source code

Python 3.10 or newer is needed.

```bash
make install    # creates .venv, installs pygame-ce, mazegenerator, flake8, mypy, pytest
make run        # runs: .venv/bin/python pac-man.py config.json
```

Other rules:

```bash
make lint          # flake8 + mypy
make lint-strict   # flake8 + mypy --strict
make debug         # runs the game with pdb
make clean         # removes caches
.venv/bin/python -m pytest tests/ -v   # unit tests
```

### Controls

| Key | Action |
|---|---|
| Arrow keys or WASD | Move |
| P or Esc | Pause |
| Arrow keys + Enter | Choose in the menu |
| Close the window | Quit (or choose Quit in the menu) |
| 1 to 5 | Cheats: invincibility, skip level, freeze cats, extra life, double speed |

## Configuration

The config is a JSON file. Lines starting with `#` are comments.

```json
# Pac-Man configuration
{
    "lives": 3,
    "seed": 42,
    "level_max_time": 90,
    "levels": [
        {"width": 15, "height": 11},
        {"width": 20, "height": 15}
    ]
}
```

| Key | Default | Allowed values | Meaning |
|---|---|---|---|
| `highscore_filename` | `highscores.json` | non-empty text | File for the top 10 |
| `lives` | 3 | 1 – 9 | Lives at the start |
| `points_per_pacgum` | 10 | 1 – 1000 | Points for a leaf |
| `points_per_super_pacgum` | 50 | 1 – 1000 | Points for a carrot |
| `points_per_ghost` | 200 | 1 – 10000 | Points for a frightened cat |
| `seed` | 42 | 1 or more | Seed of the first maze |
| `level_max_time` | 90 | 10 – 600 | Seconds to finish a level |
| `player_speed` | 6 | 1 – 15 | Cells per second |
| `ghost_speed` | 5 | 1 – 15 | Cells per second |
| `frightened_ghost_speed` | 3 | 0.5 – 15 | Cells per second when frightened |
| `frightened_time` | 7 | 1 – 30 | Seconds the cats stay frightened |
| `ghost_respawn_time` | 5 | 1 – 30 | Seconds before an eaten cat comes back |
| `levels` | 10 × (20 × 20) | width 15 – 30, height 11 – 20 | Maze size of each level |

What happens with a wrong config (the game never crashes):

- Missing key: the default is used.
- Wrong type (for example text instead of a number): the default is used, with a warning in the log.
- Too small or too big: the closest limit is used, with a warning.
- Unknown key: ignored.
- Less than 10 levels: default levels are added at the end.
- Missing file, not JSON, or broken JSON: a message, then all defaults are used.

<!-- TODO Elvira: please check this section, it is written from data/config.py -->

## Highscore

<!-- TODO Elvira: how the top 10 works (file format, name check, what happens
     with a missing or broken file) and why you chose this way. -->

## Maze Generation

We use the A-Maze-ing package assigned to us (`mazegenerator` 2.1.0, in `vendor/`).

- Call: `MazeGenerator(size=(width, height), seed=seed)`. The README of the
  package is wrong about this, so we read its code.
- The maze is a grid read as `maze[y][x]`. Each cell is a number where each bit
  is a wall: N = 1, E = 2, S = 4, W = 8. A cell with all walls (15) is part of
  the "42" pattern and is not walkable.
- The package calls `random.seed()` on Python's shared `random`, so our code
  uses its own `random.Random()` for its random choices.

<!-- TODO Elvira: how maze_loader.py uses the package (size checks, seed for
     level 1, random seeds for the next levels). -->

## Implementation

### Game loop

<!-- TODO Elvira: game.py and app.py (update order, collisions, levels, time,
     cheats, screens). -->

Each frame: read the keys → update the data (player, ghosts, rules) →
draw everything again → show the frame. Movement uses `dt`, the time since
the last frame, so the speed does not depend on the frame rate.

### Ghosts (`game/ghost.py`, `game/ghost_ai.py`)

- **Chase:** a breadth-first search (BFS) from the ghost to the rabbit.
  `next_step(maze, start, target)` returns only the first cell of the
  shortest path, because the rabbit keeps moving. A `deque` is the queue,
  a `set` keeps visited cells, a `dict` remembers which cell found each cell.
  If the target can't be reached, the ghost stays in place.
- **Run away:** a frightened ghost finds the BFS step toward the rabbit,
  then picks at random one of the other open neighbours.
  In a dead end it has no choice and takes that step.
- **States:** each ghost has a state and a timer.
  `CHASE → FRIGHTENED` (the rabbit eats a carrot, another carrot restarts the timer),
  `FRIGHTENED → EATEN` (the rabbit eats the ghost), `FRIGHTENED → CHASE` (time is over),
  `EATEN → CHASE` (after `ghost_respawn_time`, back at its spawn corner).
- **Speed:** time is collected in a move timer. Each time it reaches
  `1 / speed` seconds, the ghost moves one cell and the leftover time is kept.
  A speed of 0 or less means the ghost does not move.
- **Blinking:** `is_blinking` is true in the last 2 seconds of FRIGHTENED.

### Drawing (`ui/game_view.py`, `ui/sprites.py`)

- `draw(screen, game, sprites)` is the only drawing call the app makes.
  What `game` must have is written as a `GameView` Protocol, so mypy checks it.
- Order: maze → leaves and carrots → cats → rabbit (the rabbit is always on top).
- The whole screen is drawn again every frame: the data changes, the drawing follows.
- Walls and the "42" pattern are lines and rectangles. Tile size 36 px,
  20 px margin, 48 px HUD on top.
- Every sprite is loaded once. A missing or broken image becomes a pink square
  with a warning, so the game does not crash.
- Only pygame features that exist in MLX are used (window, images,
  rectangles, text, keyboard, clock). No rotation and no scaling.

### Packaging

The game is packaged with PyInstaller as one executable, `pac-man`,
built on school Linux (PyInstaller only builds for the system it runs on).
In the package, the images are found with `sys._MEIPASS`.
`config.json` and `INSTRUCTIONS.txt` are next to the executable.

### Tests

Unit tests with pytest in `tests/`: walls (`grid.py`), BFS and running away
(`ghost_ai.py`), ghost speed, direction, states, respawn and blinking (`ghost.py`).
The full game is checked by hand with the
[acceptance test plan](docs/project_management/test_plan.md).

## General Software Architecture

```
pac-man.py              entry point: checks the argument, starts the app
data/
  config.py             reads and checks the config file
game/                   game logic, no pygame (can be tested alone)
  grid.py               wall bits, directions, can_move
  maze_loader.py        builds the maze with mazegenerator
  player.py             player position and movement
  ghost.py              Ghost class: state, timers, movement
  ghost_ai.py           BFS chase and run away
  session.py            score, lives, level, time left
  actions.py            keyboard actions
  game.py               one level: rules, collisions, cheats
ui/                     everything with pygame
  app.py                window, game loop, screens
  game_view.py          draws the maze, items, ghosts and player
  sprites.py            loads the images
  hud.py                score, lives, level, time
  screens/              menu, pause, high scores, end screens
tests/                  pytest unit tests
assets/                 sprites and font
```

How the parts work together:

```
pac-man.py → data/config.py (Config)
           → ui/app.py ──→ game/game.py ──→ player.py, ghost.py → ghost_ai.py → grid.py
                 │                │
                 │                └──→ session.py, maze_loader.py → mazegenerator
                 └──→ ui/game_view.py.draw(screen, game, sprites)
                 └──→ ui/hud.py, ui/screens/
```

- `game/` never imports from `ui/`, so the game logic works and is tested without a window.
- One owner per file (see [team.md](docs/project_management/team.md)).

<!-- TODO Elvira: check the names of your files and classes when they are done. -->

## Project Management

We worked as a team of two, one owner per file, with a branch each.
A pull request goes into `main` only after the other one reviews it.
Tasks were on Asana (week 1), then on a GitHub Projects board.

Everything is in [docs/project_management/](docs/project_management/):

- [team.md](docs/project_management/team.md): who does what, how we worked
- [timeline.md](docs/project_management/timeline.md): plan, milestones and plan changes
- [progress.md](docs/project_management/progress.md): what was done each week
- [decisions.md](docs/project_management/decisions.md): main choices and why
- [risks.md](docs/project_management/risks.md): problems we met and what we did
- [test_plan.md](docs/project_management/test_plan.md): how we test every feature by hand

## Resources

- pygame-ce documentation: https://pyga.me/docs/
- Python `collections.deque`: https://docs.python.org/3/library/collections.html#collections.deque
- Breadth-first search: https://en.wikipedia.org/wiki/Breadth-first_search
- Red Blob Games, introduction to pathfinding: https://www.redblobgames.com/pathfinding/a-star/introduction.html
- The Pac-Man Dossier (how the original ghosts behave): https://www.gamedeveloper.com/design/the-pac-man-dossier
- PyInstaller documentation: https://pyinstaller.org/en/stable/
- pytest documentation: https://docs.pytest.org/
- mypy documentation: https://mypy.readthedocs.io/

<!-- TODO Elvira: add the resources you used. -->

### How AI was used

**Jisoo** used Claude (Anthropic) as a tutor:

- To explain new concepts step by step: `dt` timing, `typing.Protocol`, pytest.
- To give hints and questions instead of full answers. The ghost code
  (`ghost_ai.py`, `ghost.py`) and the drawing code
  (`game_view.py`, `sprites.py`) were written by Jisoo, and then reviewed with AI.
- To suggest test cases. The tests were written by Jisoo.
- To help write some docstrings and the English of the docs
  (`docs/project_management/`, `INSTRUCTIONS.txt`, this README).
- To plan the weeks and prepare messages to the team.

The sprites were drawn by hand, except rabbit.

**Elvira**:

<!-- TODO Elvira: how you used AI, for which tasks and which parts. -->
