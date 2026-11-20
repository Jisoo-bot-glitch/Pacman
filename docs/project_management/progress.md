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

## Next week (Jisoo)
- `ghost_ai.py`: BFS chase, speed, flee
- `ghost.py`: states and timers
- Tests, rabbit sprites for the other directions