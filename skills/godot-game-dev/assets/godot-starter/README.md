# Godot starter (4.x, GL Compatibility, portrait 720x1280)

**Status: UNVERIFIED in the editor.** This project was written without a Godot binary available. It has been re-read carefully but never opened, imported, run or exported. Run the commands below before trusting it, and fix anything they report. Details in `../../references/validation-status.md`.

## What is in here

```
project.godot            GL Compatibility, 720x1280 portrait, stretch canvas_items/expand,
                         etc2/astc import flag on, touch emulation from mouse
autoload/events.gd       Autoload "Events": signal bus only
autoload/game_state.gd   Autoload "GameState": score/taps/level, versioned save/load (v2, migrates v1)
scenes/main.tscn + .gd   Tap loop: tap button, score + level labels, reset button
tests_dev/test_gamestate.gd   Headless test (extends SceneTree)
icon.svg  .gitignore
```

File names are snake_case per the official GDScript style guide; the autoload names (`Events`, `GameState`) are what code uses.

## Smoke commands (run in this directory)

```bash
# 1. First time only: import resources so .godot/ exists
godot --headless --path . --import

# 2. Smoke: run the main scene for 3 frames; any output from grep = failure
godot --headless --path . --quit-after 3 2>&1 | grep -E "SCRIPT ERROR|Parse Error|nonexistent"

# 3. Unit test (exit code 0 = pass)
godot --headless -s tests_dev/test_gamestate.gd; echo "exit=$?"

# 4. Optional: open in the editor and press F5
godot --path . -e
```

Expected for step 3: 13 `ok` lines and `13 checks, 0 failures` (the count changes if you edit the tests).

## Using it as a base

1. Copy the folder, rename `config/name` in `project.godot`.
2. Replace the tap loop in `scenes/main.*` with your core loop; keep the `Events` / `GameState` pattern.
3. Put numbers in JSON (see `../../references/data-driven-config.md`), not in code.
4. Android export: see `../../references/android-export.md` (links to `rebuild-build-release`).
5. Before committing: confirm `.gitignore` excludes `.godot/` and any keystore.
