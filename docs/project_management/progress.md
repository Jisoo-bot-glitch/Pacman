# Progress

## Week 1 (Nov 11–17)

### Jisoo
- Tested pygame on Python 3.14: it fails to install, so we use pygame-ce
  (same `import pygame`). Checked on Mac and school Linux.
- Studied the assigned mazegenerator package: real call, (x, y) order,
  wall bits (N=1, E=2, S=4, W=8), "42" cells = 15, global random seed.
- Wrote the day-1 decisions and the file ownership tree with Elvira.
- `game/grid.py`: directions, `can_move`, `ALL_WALLS`.
- `game/ghost.py`: skeleton (states and `Ghost` class).
- Packaging practice: PyInstaller build on school Linux, fixed missing
  assets with `BASE_DIR` and `--add-data`, uploaded a draft to itch.io,
  downloaded it and ran it.
- `ui/game_view.py`: `window_size`, `cell_to_pixel`, `draw_maze`,
  `draw_pacgums`, `draw_ghosts`, `draw_player`, fish decoration on the "42".
- `ui/sprites.py`: loads every sprite once into a dict.
- Sprites: rabbit, 4 cats, frightened cats (blue and white), leaf, carrot, 2 fish.
- `try_view.py`: temporary demo with fake data.
- Reviewed Elvira's first PR.
- `game/ghost_ai.py`: `neighbors` and `next_step` (BFS chase). First solved
  a 3×3 maze by hand on paper, then wrote the code and checked it gives the
  same answer. Passes `mypy --strict`.
- `try_view.py`: press Space and the 4 ghosts move one cell toward the rabbit.
  They go around the "42" and never enter dead ends.
- Planned vs actual: BFS was planned for week 2, started and done on Nov 16.
- `game/ghost.py`: `speed` and `update(maze, target, dt)`. Ghosts move by
  themselves, one cell every 1 / speed seconds, using `dt` from the clock,
  so the speed does not depend on the frame rate.
- Planned vs actual: ghost speed was planned for Nov 18, done on Nov 16.

![Week 1 timeline](images/asana_timeline_week1.png)

### Elvira
- (to fill)

## Week 2 (Nov 18–24)

### Jisoo
- Reviewed and approved Elvira's PR #2. Both PRs merged into `main`,
  and `main` is now protected (a PR and 1 approval are needed).
- `game/ghost.py`: ghost states CHASE, FRIGHTENED and EATEN, each with a timer.
  `frighten()`, `get_eaten()`, respawn at the spawn corner, `is_blinking`.
- `game/ghost_ai.py`: `run_away_step`. A frightened ghost avoids the BFS step
  toward the rabbit and picks another open cell at random.
- `ui/game_view.py`: frightened cats are drawn blue and blink white in the
  last 2 seconds. Eaten cats are not drawn.
- `try_view.py`: arrow keys move the rabbit, F frightens the cats, E eats them,
  and a simple collision costs a life.
- Tests: 20 tests for `grid.py`, `ghost_ai.py` and `ghost.py`. All pass,
  with `flake8` and `mypy --strict`.
- Found a crash with a test: a frightened speed of 0 divided by zero.
  Wrote the failing test first, then fixed the speed check.
- `INSTRUCTIONS.txt` for the itch.io package, with Elvira's keys and high scores.
- Docs: decisions and risks updated.
- Planned vs actual: flee, states, timers and tests are done.
  Rabbit sprites for the other directions are not done yet (nice to have).
- The Asana trial ended, so we are moving to a GitHub Projects board.

![Week 2 board](images/github_board_week2.png)


### Elvira
- (to fill)

## Next week (Jisoo)
- `pac-man.spec` and a practice build on school Linux
- Friday: connect my part with Elvira's `game.py` and `app.py`
- Weekend: play-test together, tune speeds and times in the config
- Final build on school Linux, itch.io page
- README sections, test plan