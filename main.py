import time
import random as rdm
import pyautogui as gui
import keyboard as kb

running = True
screen_width, screen_height = gui.size()
gui.FAILSAFE = False

PATTERNS = [
    lambda: (rdm.randint(-100, 100), rdm.randint(-100, 100)),
    lambda: (rdm.randint(-300, 300), rdm.randint(-300, 300)),
    lambda: (0, 0),
    lambda: (rdm.randint(-50, 50), rdm.randint(-50, 50)) * 2,
    lambda: (rdm.choice([-200, 200]), rdm.choice([-200, 200])),
]

def on_event(event):
    global running
    if event.name == 'esc':
        print("Shutting down")
        running = False

def reset_cursor_position():
    try:
        gui.moveTo(screen_width // 2, screen_height // 2, duration=0.3)
        print("Cursor reset to screen center")
    except Exception as e:
        print(f"Error resetting cursor: {e}")
        time.sleep(1)
        try:
            gui.moveTo(screen_width // 2, screen_height // 2, duration=0.3)
        except:
            pass

def random_move_cursor():
    try:
        pattern = rdm.choice(PATTERNS)
        move_x, move_y = pattern()

        current_x, current_y = gui.position()
        target_x = max(0, min(current_x + move_x, screen_width))
        target_y = max(0, min(current_y + move_y, screen_height))

        duration = rdm.uniform(0.2, 0.8)

        print(f"Moving cursor to ({target_x}, {target_y}) over {duration:.2f}s")
        gui.moveTo(target_x, target_y, duration=duration)

        if rdm.random() < 0.05:
            for _ in range(3):
                shake_x = rdm.randint(-20, 20)
                shake_y = rdm.randint(-20, 20)
                gui.moveRel(shake_x, shake_y, duration=0.1)

    except Exception as e:
        print(f"Movement error: {e}")
        reset_cursor_position()

def move_cursor():
    while running:
        try:
            wait_time = rdm.uniform(0.5, 2.0)
            time.sleep(wait_time)

            print(f"Moving cursor after {wait_time:.2f}s wait...")
            random_move_cursor()
            print("Moving cursor done.")

            if rdm.random() < 0.1:
                pause_time = rdm.uniform(2.0, 4.0)
                print(f"Taking a longer break: {pause_time:.2f}s")
                time.sleep(pause_time)

        except Exception as e:
            print(f"Error in main loop: {e}")
            reset_cursor_position()
            time.sleep(1)

if __name__ == "__main__":
    kb.on_press(on_event)
    try:
        move_cursor()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        exit(0)