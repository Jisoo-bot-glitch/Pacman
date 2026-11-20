# Acceptance test plan

| # | Feature | How to test | Expected | Result | Bug found / fixed |
|---|---|---|---|---|---|
| 1 | Player can't go through walls | Push the arrow key into a wall | The rabbit stays in place | ✅ | — |
| 2 | Eating a pacgum | Walk onto a leaf | Leaf disappears, score +10 | ✅ | — |
| 3 | Super-pacgum | Eat a carrot | Cats turn blue and run away for 7 s | ❌ → ✅ | Cats kept chasing: state not set. Fixed in ghost.py |
| 4 | Packaged game | Download from itch.io, run on school Linux | Game starts without Python installed | ✅ | assets not found → fixed with BASE_DIR |