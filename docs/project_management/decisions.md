# Decisions

Main choices we made, why, and who decided.
Most of them come from our day-1 meeting (Nov 10–11). Later changes are dated.

## Technology

| Date | Decision | Why | Who |
|---|---|---|---|
| Nov 11 | Use **pygame-ce** instead of pygame (code still uses `import pygame`) | pygame does not install on Python 3.14 (no prebuilt package, it needs SDL to compile). pygame-ce installs on Mac and on school Linux | Jisoo proposed, both agreed |
| Nov 11 | Only use pygame features that have an MLX equivalent: window, images, rectangles, text, keyboard, clock. No rotate, no scale, no sound | Subject chapter 4 |  -  |
| Nov 11 | One sprite per direction instead of rotating images | Rotation is not allowed (see above) |  -  |

## Game rules

| Date | Decision | Why | Who |
|---|---|---|---|
| Nov 11 | Tile-based movement (positions are always cells), 60 FPS | Simple and easy to test. Smooth drawing can be added later only in `game_view.py` | Both |
| Nov 11 | Pacgums on every walkable cell except the start, super-pacgums in the 4 corners | Classic Pac-Man layout | Both |
| Nov 11 | Our code uses its own `random.Random()` | The assigned package calls `random.seed()` on Python's shared random | Both |
| Nov 16 | Ghosts chase with BFS (shortest path). `next_step(maze, start, target)` returns only the next cell, and takes any target cell | Subject 6.3 lets us choose the chase behavior. Only one step, because the player keeps moving. Any target, so eaten ghosts can go back to their corner and personalities can be added later | Jisoo |
| Nov 16 | BFS queue is a `deque`, visited cells a `set`, arrows a `dict` | `popleft()` is fast, "already visited?" is fast, and arrows are pairs (cell → cell that found it) | Jisoo |
| Nov 17 | Ghost speed 0 or less = the ghost does not move (and its timer does not fill up) | No ZeroDivisionError, and no sudden jump after the freeze cheat ends | Elvira asked, Jisoo |
| Nov 20 | Ghost states: CHASE → FRIGHTENED (rabbit eats a carrot) → EATEN (rabbit eats the ghost) → CHASE. Another carrot restarts the frightened timer | One state at a time, each with its own timer. Easy to test | Jisoo |
| Nov 20 | An eaten ghost disappears, then comes back at its spawn corner after `respawn_time` | Simpler than drawing eyes walking home, same effect in the game | Jisoo |
| Nov 21 | Frightened ghosts run away: find the BFS step toward the rabbit, then choose randomly among the other open cells. In a dead end, take that step anyway | Uses the BFS we already have, and stays simple | Jisoo |
| Nov 24 | Ghost personalities are a bonus, only if we have time at the end | Subject 6.3 lets us choose the chase behavior. Personalities are only in the Foreword | Jisoo proposed |

## Display

| Date | Decision | Why | Who |
|---|---|---|---|
| Nov 11 | Tile size **32 → 36 px** | Tested on screen before drawing sprites: 32 px looked too small | Jisoo tested, both agreed |
| Nov 11 | 20 px margin around the maze | Thick wall lines were cut at the window edge | Jisoo found it, explained to Elvira |
| Nov 13 | HUD height **40 → 48 px**, HUD font 28 | 40 px looked too small for the text and the lives icons | Jisoo proposed, Elvira agreed |
| Nov 13 | `TILE_SIZE`, `MARGIN`, `HUD_HEIGHT` live together in `ui/game_view.py` | The window size depends on all three; Elvira's HUD imports `HUD_HEIGHT` | Both |
| Nov 12 | Our own theme instead of the original Pac-Man: the player is a rabbit, pacgums are leaves, super-pacgums are carrots, ghosts are cats | Avoid copyrighted sprites, and make the game our own | Decided together, sprites drawn by Jisoo |
| Nov 13 | Two fish stickers on fixed blocks of the "42" pattern | Decoration only. Fixed blocks (counted in drawing order) so they stay on the "42" for every maze size and never flicker | Jisoo |
| Nov 16 | Drawing order: maze → pacgums → ghosts → player (player on top) | The player must always see their own character, also with the invincibility cheat | Jisoo |
| Nov 17 | Keep `pygame.draw.line` / `rect` for walls and the "42" | Students who passed confirmed it was accepted. Plan B: draw walls as small images with `blit` | Both |
| Nov 17 | A missing or broken sprite becomes a pink square, with a warning on stderr | Subject: "Robust error handling, no crash!" | Elvira asked, Jisoo |
| Nov 20 | Frightened ghosts blink (blue / white every 250 ms) in the last 2 seconds | Tells the player that the cats will chase again soon | Jisoo |

## Team workflow

| Date | Decision | Why | Who |
|---|---|---|---|
| Nov 11 | One owner per file, no shared `entities.py` (player data in `player.py`, ghost data in `ghost.py`) | Avoid merge conflicts | Both |
| Nov 11 | One branch each, PRs merged only after the other one reviews them, `main` protected | Every line is seen by both of us | Both |
| Nov 11 | Work with fake data until the other part is ready | We can work in parallel without waiting | Both |
| Nov 13 | `try_view.py`: temporary demo that draws the game with fake data | Lets us see the screen before `app.py` exists, and shows how `app.py` can call `game_view` | Jisoo |
| Nov 14 | Jisoo creates `docs/project_management/` first, each of us then fills in our own sections | Avoid both creating the same files | Jisoo |
| Nov 16 | `Position` type moved to `game/grid.py` | `game/` must not import from `ui/`, so the game logic can be tested without pygame | Jisoo |
| Nov 17 | `game_view.draw(screen, game, sprites)` is the only drawing call for app.py. What `game` must have is written as a `GameView` Protocol in `game_view.py` | One door into the drawing code, and mypy checks that Game has the right names | Elvira asked, Jisoo |
| Nov 21 | `try_view.py` has fake rules: arrow keys move the rabbit, F frightens the cats, E eats them, simple same-cell collision | Test the ghost features before `game.py` exists. The real rules will be in Elvira's `game.py` | Jisoo |