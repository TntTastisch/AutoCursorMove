import random as rdm
import time
from threading import Event

import keyboard as kb
import pyautogui as gui

shutdown_event = Event()
gui.FAILSAFE = False
gui.PAUSE = 0.1

screen_width, screen_height = gui.size()
PATTERNS = [
    lambda: (rdm.randint(-100, 100), rdm.randint(-100, 100)),
    lambda: (rdm.randint(-300, 300), rdm.randint(-300, 300)),
    lambda: (0, 0),
    lambda: (rdm.randint(-50, 50), rdm.randint(-50, 50)) * 2,
    lambda: (rdm.choice([-200, 200]), rdm.choice([-200, 200])),
    lambda: (rdm.randint(-150, 150), 0),
    lambda: (0, rdm.randint(-150, 150)),
    lambda: (rdm.choice([-100, 100]), rdm.choice([-100, 100])),
]


def on_event(event):
    if event.name == 'esc':
        print("\nShutdown initiated...")
        shutdown_event.set()


def is_cursor_in_bounds(x, y):
    return 0 <= x <= screen_width and 0 <= y <= screen_height


def reset_cursor_position():
    center_x = screen_width // 2
    center_y = screen_height // 2

    for attempt in range(3):
        if shutdown_event.is_set():
            return False
        try:
            if not is_cursor_in_bounds(*gui.position()):
                gui.moveTo(center_x, center_y, duration=0.5)
                time.sleep(0.5)
            print("Cursor reset to screen center")
            return True
        except Exception as e:
            print(f"Reset attempt {attempt + 1} failed: {e}")
            time.sleep(1)
    return False


def random_move_cursor():
    if shutdown_event.is_set():
        return

    try:
        pattern = rdm.choice(PATTERNS)
        move_x, move_y = pattern()

        current_x, current_y = gui.position()
        target_x = max(0, min(current_x + move_x, screen_width - 1))
        target_y = max(0, min(current_y + move_y, screen_height - 1))

        if not is_cursor_in_bounds(target_x, target_y):
            print("Target position out of bounds, resetting...")
            reset_cursor_position()
            return

        duration = rdm.uniform(0.3, 0.9)
        print(f"Moving cursor to ({target_x}, {target_y}) over {duration:.2f}s")

        steps = int(duration / 0.1)
        for step in range(steps):
            if shutdown_event.is_set():
                return
            progress = (step + 1) / steps
            current_target_x = current_x + (target_x - current_x) * progress
            current_target_y = current_y + (target_y - current_y) * progress
            gui.moveTo(current_target_x, current_target_y, duration=0.1)

        if rdm.random() < 0.05 and not shutdown_event.is_set():
            print("Adding trembling effect...")
            for _ in range(3):
                if shutdown_event.is_set():
                    return
                shake_x = rdm.randint(-10, 10)
                shake_y = rdm.randint(-10, 10)
                gui.moveRel(shake_x, shake_y, duration=0.1)

    except Exception as e:
        print(f"Movement error: {e}")
        if not shutdown_event.is_set():
            reset_cursor_position()


def move_cursor():
    print("Starting cursor movement (Press ESC to exit)")

    while not shutdown_event.is_set():
        try:
            if not is_cursor_in_bounds(*gui.position()):
                print("Cursor out of bounds detected")
                reset_cursor_position()
                continue

            wait_time = rdm.uniform(0.8, 2.0)
            elapsed = 0
            while elapsed < wait_time and not shutdown_event.is_set():
                time.sleep(0.1)
                elapsed += 0.1

            if shutdown_event.is_set():
                break

            print(f"Moving cursor after {wait_time:.2f}s wait...")
            random_move_cursor()

            if shutdown_event.is_set():
                break

            print("Moving cursor done.")

            if rdm.random() < 0.1 and not shutdown_event.is_set():
                pause_time = rdm.uniform(2.0, 4.0)
                print(f"Taking a longer break: {pause_time:.2f}s")
                elapsed = 0
                while elapsed < pause_time and not shutdown_event.is_set():
                    time.sleep(0.1)
                    elapsed += 0.1

        except Exception as e:
            print(f"Error in main loop: {e}")
            if not shutdown_event.is_set():
                reset_cursor_position()
                time.sleep(1)

    print("Shutdown complete!")


if __name__ == "__main__":
    kb.on_press(on_event)
    try:
        print(f"Screen size: {screen_width}x{screen_height}")
        move_cursor()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected")
        shutdown_event.set()
    finally:
        print("Exiting...")
