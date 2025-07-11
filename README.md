# Cursor Auto-Mover
A sophisticated tool that automatically moves your mouse cursor on the screen with various movement patterns.

## Quick Start
1. Double-click the `.exe` file to run
2. The cursor will start moving automatically with:
    - Random movement patterns
    - Variable timing between moves
    - Automatic error recovery
    - Screen boundary protection

## Features
- Multiple movement patterns:
    - Small random movements
    - Larger jumps
    - Occasional pauses
    - Trembling movements
    - Diagonal jumps
    - Horizontal movements
    - Vertical movements
    - Directed jumps
- Variable movement speeds (0.3-0.9 seconds per movement)
- Random wait times between movements (0.8-2.0 seconds)
- Occasional longer breaks (2-4 seconds)
- 5% chance of trembling effect with reduced amplitude
- Automatic cursor centering on errors
- Improved shutdown response

## Controls
- **ESC**: Press to stop the program cleanly (responds within 0.1 seconds)
- **Ctrl+C**: Emergency stop (in console window)

## What to Expect
- A console window showing detailed movement information
- Random cursor movements with varying patterns and speeds
- Step-by-step movement tracking in console
- Automatic recovery from errors by resetting to screen center
- Screen boundary protection to prevent cursor loss
- Immediate response to stop command

## Troubleshooting
If the program isn't working:
- Make sure you have administrator rights
- Check if your antivirus isn't blocking it
- If console closes immediately, run it from command prompt to see error messages
- If cursor gets stuck, it will automatically reset to screen center
- If shutdown seems slow, press ESC again (though one press should be sufficient)

## Notes
- Keep the console window open while running
- The program has built-in error handling and recovery
- Movements are designed to be unpredictable but safe
- Program responds quickly to ESC key
- Movement patterns are smoothly interpolated
- Built-in failsafe mechanisms prevent cursor from getting stuck

That's all you need to know! Just run and press ESC when you want to stop.