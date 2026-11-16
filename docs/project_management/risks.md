# Risks and blocking points

Problems we met (or expected), what they could break, and what we did.

| # | Risk / problem | Impact | What we did | Status |
|---|---|---|---|---|
| 1 | pygame does not install on Python 3.14 (no prebuilt package, needs SDL to compile) | Nobody can run the game | Switched to pygame-ce, same `import pygame`. Tested on Mac and school Linux | ✅ Solved |
| 2 | The assigned mazegenerator package's README is wrong (real call is `MazeGenerator(size=(w, h), ...)`), and it does not check its input | Crashes or wrong mazes | Read its code, wrapped it in `maze_loader.py` with checks and a default size | ✅ Understood, wrapper planned |
| 3 | The package calls `random.seed()` on Python's shared random | Our random choices would always be the same | Our code uses its own `random.Random()` | ✅ Solved |
| 4 | Subject forbids functions without an MLX equivalent | A feature could be refused at evaluation | No scale, no rotate, one sprite per direction | ✅ Rule followed |
| 5 | Wall lines were cut at the window edge | Ugly display | Added a 20 px margin. This changed the window size, so we shared the new numbers right away | ✅ Solved |
| 6 | Tile size changed (32 → 36) | Sprites must match the tile exactly | Changed it before drawing any sprite | ✅ Solved |
| 7 | Copyrighted Pac-Man sprites and fonts | Problems when publishing on itch.io | Our own sprites, and a font with a licence that allows publishing (SIL OFL) | ✅ Solved |
| 8 | PyInstaller only builds for the OS it runs on | A Mac build would not run on Linux | Final build will be made on school Linux | ⏳ Planned |
| 9 | Packaged game could not find `assets/` (FileNotFoundError) | Game crashes after packaging | `BASE_DIR` from `sys._MEIPASS` / `__file__` and `--add-data "assets:assets"`. Full test: build, zip, upload to itch.io as a draft, download, run | ✅ Solved in practice |
| 10 | Players do not know the name of the executable | They cannot start the game | Final build named `pac-man`, `INSTRUCTIONS.txt` inside the package, run guide on the itch.io page | ⏳ Planned |
| 11 | Merge conflicts between our branches | Lost work, wasted time | One owner per file, shared names agreed on day 1 | ✅ No conflict so far |
| 12 | No `.gitignore` yet on Jisoo's branch, so `__pycache__` files went into PR #1 | Useless files in the repo | Removed them, add files by exact name, local ignore list (`.git/info/exclude`) until the shared `.gitignore` is merged | ✅ Solved |
| 13 | Working on two computers (home Mac and school Linux) | Old code, or a push refused by GitHub | `git pull` first every time we change computer. `.venv` made on each computer and never committed | ✅ Rule followed |
| 14 | mypy fails on mazegenerator (no type information) | `make lint-strict` fails | Add `[mypy-mazegenerator.*] ignore_missing_imports = True` to `setup.cfg` | ⏳ Proposed to Elvira |
| 15 | Reviews take time (PR #1 not reviewed after several days) | Elvira's HUD needs `HUD_HEIGHT` from PR #1 | Kept working on the same branch, reminded Elvira, review planned for Nov 17 | ⏳ In progress |


## Blocking points so far

- **Nov 11:** pygame install failure (risk 1).
- **Nov 12:** packaged game could not find its images (risk 9).