# Team

Two people: **Jisoo** (jisobaek) and **Elvira** (efatin).

## Who does what

The rule: **one owner per file**. We ask before editing the other one's file.
Shared names (positions, directions, ghost states, function names) were agreed on day 1,
so each of us can work with fake data until the other part is ready.

### Jisoo — ghosts, game drawing, packaging

| Area | Files |
|---|---|
| Wall check (shared helper) | `game/grid.py` |
| Ghost data and states | `game/ghost.py` |
| Ghost movement (BFS chase, flee) | `game/ghost_ai.py` |
| Game screen drawing (maze, pacgums, ghosts, player) | `ui/game_view.py` |
| Loading images | `ui/sprites.py` |
| Sprites (drawn on iPad) | `assets/` |
| Packaging and release | `pac-man.spec`, `INSTRUCTIONS.txt`, itch.io page |
| Tests for her files | `tests/test_grid.py`, `tests/test_ghost_ai.py` |

### Elvira — player, game rules, screens

| Area | Files |
|---|---|
| Entry point | `pac-man.py` |
| Player movement | `game/player.py` |
| Score, lives, level, time | `game/session.py` |
| Keyboard actions | `game/actions.py` |
| Ghost personalities | `game/ghost_personality.py` |
| Maze, levels, rules, cheats, game update | `game/maze_loader.py`, `game/level.py`, `game/rules.py`, `game/cheat.py`, `game/game.py` |
| Config and highscores | `config.json`, config and highscore code |
| Screen flow, input, HUD | `ui/app.py`, `ui/input.py`, `ui/hud.py` |
| Menu, highscores, instructions, pause, end screens | `ui/screens/` |
| Project setup | `Makefile`, `requirements.txt`, `setup.cfg`, `.gitignore` |

### Both

- `README.md`: each of us writes the sections about our own part.
- `docs/project_management/`: each of us fills in our own sections.

## How we made decisions

- **Day-1 (Nov 10):** Jisoo wrote a proposal (file split, shared names, game rules,
  timeline) as two PDFs. We discussed it and agreed. See [decisions.md](decisions.md).
- **Later changes:** whoever finds a problem proposes a change with the reason and the numbers,
  and the other one agrees before it is used. Example: HUD height 40 → 48 (Nov 13).
- **Shared numbers live in one place:** `TILE_SIZE`, `MARGIN` and `HUD_HEIGHT` are only in
  `ui/game_view.py`, and Elvira's HUD imports them.

## How we work with Git

- One branch each (`jisobaek`, `elvira`). `main` only gets reviewed work.
- A pull request is merged only after the other one has reviewed it.
- Review comments say what is wrong, why, and how to fix it.
- When we change computer: `git pull` first.

## How we handled issues

| Date | Issue | What we did |
|---|---|---|
| Nov 11 | pygame does not install on Python 3.14 | Jisoo tested pygame-ce on both computers and proposed it, Elvira agreed |
| Nov 11 | We had different window sizes (1080×760 vs 1120×800) | Jisoo explained the new 20 px margin; we now share practice changes right away |
| Nov 12 | `__pycache__` files went into PR #1 | Removed them; add files by exact name until the shared `.gitignore` is merged |
| Nov 13 | Review of Elvira's first PR | Found a broken `.PHONY` line and a `pbd` typo in the Makefile; asked for fixes before approving |
| Nov 13–17 | PR #1 waited for a review | Jisoo kept working on the same branch and told Elvira what was added |
| Nov 14 | Both of us would create the same docs files | Jisoo created `docs/project_management/` first, each fills in their own sections |

More details in [risks.md](risks.md).

## Tools

- **GitHub:** branches, pull requests, reviews.
- **Asana (week 1), then GitHub Projects (from week 2):** task board for both of us (see [timeline.md](timeline.md)).