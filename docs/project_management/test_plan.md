# Acceptance test plan

How we check every feature of the subject by hand, on the real game.
Unit tests (pytest) are in `tests/`. This plan is for what a player sees.

Result: ✅ works, ❌ bug found, ⏳ not tested yet.

## Start and config (subject 5.1–5.3)

| # | Feature | How to test | Expected | Result | Bug found / fixed |
|---|---|---|---|---|---|
| 1 | Exactly one argument | Run `./pac-man` with no argument, then with two | Clear error message, no traceback | ⏳ | |
| 2 | Missing config file | `./pac-man nofile.json` | Clear error message, no traceback | ⏳ | |
| 3 | Comments in config | Add a line starting with `#` | The game starts normally | ⏳ | |
| 4 | Wrong value | Set `"lives": 100` or `"lives": "abc"` | Safe value used, message in the log | ⏳ | |
| 5 | Unknown key | Add `"color": "red"` | Ignored, the game starts | ⏳ | |
| 6 | Changed config | Change `lives`, speeds and level sizes | The game uses the new values | ⏳ | |

## Gameplay

| # | Feature | How to test | Expected | Result | Bug found / fixed |
|---|---|---|---|---|---|
| 7 | Walls | Push an arrow key into a wall | The rabbit stays in place | ⏳ | |
| 8 | Pacgum | Walk onto a leaf | Leaf disappears, score +10 | ⏳ | |
| 9 | Super-pacgum | Eat a carrot | Score +50, cats turn blue and run away | ⏳ | |
| 10 | Eat a cat | Touch a blue cat | Score +200, the cat disappears, comes back at its corner later | ⏳ | |
| 11 | Caught by a cat | Touch a cat that chases | One life less, the rabbit starts again | ⏳ | |
| 12 | Level end | Eat all the leaves | Next level, new maze | ⏳ | |
| 13 | First maze | Start the game twice | Level 1 is the same maze (seed 42) | ⏳ | |
| 14 | Time limit | Wait until the time runs out | One life less, the timer restarts | ⏳ | |
| 15 | Game over | Lose all lives | Game over screen | ⏳ | |
| 16 | 10 levels | Skip levels with the cheat key | 10 levels, then the end screen | ⏳ | |

## Ghosts

| # | Feature | How to test | Expected | Result | Bug found / fixed |
|---|---|---|---|---|---|
| 17 | Chase | Move away from the cats | Cats follow the rabbit by the shortest way | ⏳ | |
| 18 | Run away | Eat a carrot | Blue cats move away from the rabbit | ⏳ | |
| 19 | Blinking | Wait after eating a carrot | Cats blink blue / white in the last 2 seconds | ⏳ | |
| 20 | Back to chase | Wait until the blinking ends | Cats chase again | ⏳ | |

## Screens and HUD

| # | Feature | How to test | Expected | Result | Bug found / fixed |
|---|---|---|---|---|---|
| 21 | HUD | Play | Score, lives, level and time are shown and change | ⏳ | |
| 22 | Menu | Use arrows + Enter | Every menu item works | ⏳ | |
| 23 | Pause | Press P or Esc | The game stops, then goes on | ⏳ | |
| 24 | Quit | Close the window | The game ends, no traceback | ⏳ | |
| 25 | High scores | Finish a game with a good score | Type a name, it is saved in the top 10 | ⏳ | |
| 26 | Broken high score file | Write random text in `highscores.json` | The game starts, no crash | ⏳ | |

## Cheats

| # | Feature | How to test | Expected | Result | Bug found / fixed |
|---|---|---|---|---|---|
| 27 | Cheat keys | Press 1 to 5 one by one | Each cheat works, "CHEAT" is shown | ⏳ | |

## Errors and packaging

| # | Feature | How to test | Expected | Result | Bug found / fixed |
|---|---|---|---|---|---|
| 28 | Missing sprite | Rename one image in `assets/` | A pink square instead, warning in the terminal, no crash | ⏳ | |
| 29 | Packaged game | Download from itch.io, run on school Linux | The game starts without Python installed | ✅ (practice build, Nov 12) | `assets/` not found → fixed with `BASE_DIR` |
| 30 | Final package | Same test with the final build | The game starts, all assets found | ⏳ | |