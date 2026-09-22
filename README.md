# Cursor Auto-Mover

A small tool that automatically moves your mouse cursor across the screen using
various movement patterns. Useful for keeping a machine "active" (anti-idle),
demos, or testing.

## Download
Prebuilt binaries for Windows, Linux and macOS are attached to every
[release](https://github.com/TntTastisch/AutoCursorMove/releases) and are built
automatically whenever a version tag is pushed. Download the file for your
platform and run it — no Python installation required. To run from source
instead, see [Quick Start](#quick-start) below.

## Requirements
- Python 3.8+
- The dependencies listed in `requirements.txt` (mainly [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) and [keyboard](https://pypi.org/project/keyboard/))

Install them with:
```
pip install -r requirements.txt
```

> On Linux the `keyboard` library needs root privileges to capture the ESC key.
> On Windows this is usually not required.

## Quick Start
Run the program from source:
```
python main.py
```
A small window (showing the application icon) opens where you can pick a movement
pattern. As soon as you click a pattern, the window closes and the cursor starts
moving. Press **ESC** at any time to stop.

## Movement Patterns
| Key          | Pattern                     | Description                                              |
|--------------|-----------------------------|----------------------------------------------------------|
| `small`      | Small random movement       | Offsets of -100..100 px on both axes                     |
| `large`      | Large random movement       | Offsets of -300..300 px on both axes                     |
| `horizontal` | Horizontal movement         | Moves left/right only (-150..150 px)                     |
| `vertical`   | Vertical movement           | Moves up/down only (-150..150 px)                        |
| `diagonal`   | Diagonal jumps              | Fixed ±200 px jumps on both axes                         |
| `tremble`    | Trembling in place          | Tiny jitter of -15..15 px                                |
| `adhs`       | ADHD mode                   | Large, fast jumps across half the screen                 |
| `pause`      | No movement (pause)         | Cursor stays put                                         |

Movements are smoothly interpolated. Normal patterns use a per-move duration of
~0.4–1.2 s with a 1–3 s wait between moves; the `adhs` pattern runs continuously
with a ~0.05–0.15 s duration per move.

## Command Line
You can preselect a pattern and skip the selection window:
```
python main.py --pattern large      # start immediately with the "large" pattern
python main.py --list-patterns      # print all available pattern keys and exit
```
Available keys: `small`, `large`, `horizontal`, `vertical`, `diagonal`,
`tremble`, `adhs`, `pause`.

## Controls
- **ESC**: Stop the movement cleanly (once the GUI has closed / movement has started)
- **Ctrl+C**: Emergency stop from the console
- **Move the mouse yourself**: the automation pauses and resumes shortly after you stop (see [Manual Override](#manual-override))
- Closing the pattern window exits the program

## Manual Override
You stay in control at all times. If you move the mouse yourself while a pattern
is running, the tool notices the cursor being pulled away from where it left it
and **pauses** the automation. It resumes automatically once the mouse has been
still for about 3 seconds, so it never fights you for the pointer. This works for
every pattern, including the fast `adhs` mode.

## Safety & Recovery
- Cursor stays within the screen bounds; if it ever ends up out of bounds it is
  reset to the screen center.
- `pyautogui.FAILSAFE` is disabled so the program does not abort when the cursor
  reaches a screen corner — use **ESC** to stop instead.
- Built-in error handling keeps the loop running and recenters the cursor on
  unexpected errors.

## Troubleshooting
- If the console closes immediately, run it from a terminal to see error output.
- Make sure the dependencies are installed (`pip install -r requirements.txt`).
- On Linux, run with the privileges needed for the `keyboard` library to capture ESC.
- If the cursor seems stuck, it will automatically reset to the screen center.
