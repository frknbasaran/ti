# Slots & Skulls wiki data

The wiki at `/slots-and-skulls/wiki/` is built from JSON that this script generates
from the game's Unity project. Nothing in `src/data/wiki/` is written by hand: if a
number or a sentence on the wiki is wrong, fix it in the game and run the script again.

## Run it

```sh
python3 -I scripts/wiki/extract.py /path/to/SLOTS_AND_ANVIL
```

Options:

- `--site PATH`: the website root to write into (default: this repo).
- `--report FILE`: also write the full report (what was left out and why, icons
  that were not exported and their source files) to a JSON file. Keep it outside
  the repo: it names spoilers and third-party asset paths.

Requirements: Python 3.10+, Pillow and PyYAML. The project is only read, never written.

Then build the site as usual (`npm run build`).

## What it reads

- `Assets/_Project/Data/**.asset` for symbols, powerups, modifiers, cats, enemies,
  levels, challenges and reinforcements, plus `GameConfig`, `UpgradeConfig`,
  `GameDatabase` and `DuelRanks`. Only content registered in `GameDatabase` is used.
- `Assets/_Project/Data/localization.csv`, English column, for names, card texts and
  in-game hints.
- A few rules that live in C# rather than in assets: enum orders, the effect card
  text templates (`EffectDef.Describe`, ported to Python so every forge level +0 to
  +10 can be printed), boss threats and their answers (`BossThreats`), symbol groups
  (`SymbolGroups`), demo limits (`DemoGate`), duel ranks (`DuelRank`), 1v1 numbers
  (`PvpRuleset`) and the Steam achievement list (`AchievementCatalog`). If one of
  these moves or changes shape, the script stops with an error instead of guessing.

The script checks its card text port against `localization.csv` at +0 and prints any
symbol where the two differ.

## What it writes

- `src/data/wiki/*.json`: one file per category, plus `rules.json` (config tables,
  odds, in-game hints) and `meta.json` (counts and a hash of the source data).
- `public/wiki/icons/`: pixel art at its original size, rendered from the studio's
  own Aseprite files (enemies, cats, gems). The folder is recreated on every run.

## Left out on purpose

- Icons from third-party packs. `Assets/Icons` and `Assets/_Project/Art` hold copies
  of pack art (for example RPG Icons Pixel Art, Rank Emblems 48x48), so symbols,
  powerups, modifiers, reinforcements and duel ranks show a neutral placeholder.
  Only `Assets/Aseprite` counts as own art (`OWN_ART_DIRS` in `extract.py`).
- The final boss and its phases (spoiler), achievements the game marks as hidden,
  pacts no cat offers, assets not registered in `GameDatabase`, and in-game tips that
  use wording the studio retired (`RETIRED_PHRASES`).
