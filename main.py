import argparse
import random as rdm
import time
import tkinter as tk
from tkinter import ttk
from threading import Event, Thread

import keyboard as kb
import pyautogui as gui


shutdown_event = Event()
exit_program_event = Event()
selected_pattern_func = None
gui.FAILSAFE = False
gui.PAUSE = 0.05

screen_width, screen_height = gui.size()


PATTERNS = [
    {
        "key": "small",
        "name": "Small random movement",
        "func": lambda: (rdm.randint(-100, 100), rdm.randint(-100, 100)),
    },
    {
        "key": "large",
        "name": "Large random movement",
        "func": lambda: (rdm.randint(-300, 300), rdm.randint(-300, 300)),
    },
    {
        "key": "horizontal",
        "name": "Horizontal movement",
        "func": lambda: (rdm.randint(-150, 150), 0),
    },
    {
        "key": "vertical",
        "name": "Vertical movement",
        "func": lambda: (0, rdm.randint(-150, 150)),
    },
    {
        "key": "diagonal",
        "name": "Diagonal jumps",
        "func": lambda: (rdm.choice([-200, 200]), rdm.choice([-200, 200])),
    },
    {
        "key": "tremble",
        "name": "Trembling in place",
        "func": lambda: (rdm.randint(-15, 15), rdm.randint(-15, 15)),
    },
    {
        "key": "adhs",
        "name": "ADHS MODUS",
        "func": lambda: (
            rdm.randint(-screen_width // 2, screen_width // 2),
            rdm.randint(-screen_height // 2, screen_height // 2),
        ),
        "fast_mode": True,
    },
    {"key": "pause", "name": "No movement (pause)", "func": lambda: (0, 0)},
]


gui_closed = False


def on_shutdown_event(event):
    global gui_closed

    if event.name == "esc" and gui_closed is False:
        print("ESC ignored, GUI is still open.")
        return
    if event.name == "esc" and not shutdown_event.is_set():
        print("\nESC pressed, stopping movement...")
        shutdown_event.set()
        gui_closed = True


def is_cursor_in_bounds(x, y):
    return 0 <= x <= screen_width and 0 <= y <= screen_height


def reset_cursor_position():
    if shutdown_event.is_set():
        return
    center_x, center_y = screen_width // 2, screen_height // 2
    try:
        if not is_cursor_in_bounds(*gui.position()):
            print("Cursor out of bounds. Resetting position.")
            gui.moveTo(center_x, center_y, duration=0.5)
            time.sleep(0.5)
    except Exception as e:
        print(f"Error resetting cursor: {e}")


def random_move_cursor():
    if shutdown_event.is_set() or not selected_pattern_func:
        return
    try:
        move_x, move_y = selected_pattern_func()
        current_x, current_y = gui.position()
        target_x = max(0, min(current_x + move_x, screen_width - 1))
        target_y = max(0, min(current_y + move_y, screen_height - 1))

        fast_mode = False
        for pattern in PATTERNS:
            if pattern.get("func") == selected_pattern_func and pattern.get(
                "fast_mode"
            ):
                fast_mode = True
                break
        if fast_mode:
            duration = rdm.uniform(0.05, 0.15)
        else:
            duration = rdm.uniform(0.4, 1.2)
        gui.moveTo(target_x, target_y, duration=duration, tween=gui.easeInOutQuad)
    except Exception as e:
        print(f"Error during movement: {e}")
        reset_cursor_position()


def move_cursor_loop():
    print("Mouse movement loop started (ESC to exit)")
    fast_mode = False
    for pattern in PATTERNS:
        if pattern.get("func") == selected_pattern_func and pattern.get("fast_mode"):
            fast_mode = True
            break
    while not shutdown_event.is_set():
        try:
            if not is_cursor_in_bounds(*gui.position()):
                reset_cursor_position()
            random_move_cursor()
            if not fast_mode:
                wait_time = rdm.uniform(1.0, 3.0)
                shutdown_event.wait(wait_time)

        except Exception as e:
            print(f"Error in main loop: {e}")
            reset_cursor_position()
            time.sleep(1)
    print("Mouse movement loop ended.")


def start_movement(pattern_func, root):
    global selected_pattern_func, gui_closed
    selected_pattern_func = pattern_func
    gui_closed = True
    print(f"Pattern selected. Starting movement...")
    if hasattr(root, "after_id") and root.after_id:
        root.after_cancel(root.after_id)
    root.destroy()
    kb.unhook_all()
    kb.on_press(on_shutdown_event)
    movement_thread = Thread(target=move_cursor_loop, daemon=True)
    movement_thread.start()


def start_movement_headless(pattern_func):
    global selected_pattern_func, gui_closed
    selected_pattern_func = pattern_func
    gui_closed = True
    kb.unhook_all()
    kb.on_press(on_shutdown_event)
    move_cursor_loop()


def find_pattern(key):
    for pattern in PATTERNS:
        if pattern["key"] == key.lower():
            return pattern
    return None


def parse_args():
    parser = argparse.ArgumentParser(description="Automatically move the mouse cursor.")
    parser.add_argument(
        "-p",
        "--pattern",
        choices=[p["key"] for p in PATTERNS],
        help="start immediately with this movement pattern (skips the GUI)",
    )
    parser.add_argument(
        "--list-patterns", action="store_true", help="list available patterns and exit"
    )
    return parser.parse_args()


def create_gui():
    global gui_closed
    gui_closed = False
    root = tk.Tk()
    root.title("Mausbewegungs-Muster")
    root.geometry("500x600")
    root.resizable(False, False)
    root.configure(bg="#2E2E2E")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TButton",
        foreground="white",
        background="#555555",
        font=("Segoe UI", 10, "bold"),
        padding=10,
        borderwidth=1,
        relief="raised",
    )
    style.map(
        "TButton", background=[("active", "#6E6E6E")], foreground=[("active", "white")]
    )
    style.configure(
        "TLabel",
        background="#2E2E2E",
        foreground="#FFFFFF",
        font=("Segoe UI", 12, "bold"),
    )
    style.configure("TFrame", background="#2E2E2E")

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(expand=True, fill="both")
    title_label = ttk.Label(main_frame, text="Wähle ein Bewegungsmuster")
    title_label.pack(pady=(0, 20))

    for pattern in PATTERNS:
        button = ttk.Button(
            main_frame,
            text=pattern["name"],
            command=lambda p=pattern["func"]: start_movement(p, root),
        )
        button.pack(fill="x", pady=5)

    def on_window_close():
        global gui_closed
        print("Window closed, exiting program.")
        exit_program_event.set()
        shutdown_event.set()
        gui_closed = True

    def check_shutdown():
        if shutdown_event.is_set():
            if hasattr(root, "after_id") and root.after_id:
                root.after_cancel(root.after_id)
                root.after_id = None
            root.quit()
        else:
            root.after_id = root.after(100, check_shutdown)

    root.protocol("WM_DELETE_WINDOW", on_window_close)
    root.after_id = root.after(100, check_shutdown)
    root.mainloop()


if __name__ == "__main__":
    args = parse_args()
    if args.list_patterns:
        for pattern in PATTERNS:
            print(f"{pattern['key']:<12} {pattern['name']}")
        raise SystemExit(0)
    try:
        print(f"Screen size: {screen_width}x{screen_height}")
        if args.pattern:
            pattern = find_pattern(args.pattern)
            print(f"Pattern '{pattern['name']}' selected via --pattern.")
            start_movement_headless(pattern["func"])
        else:
            while not exit_program_event.is_set():
                shutdown_event.clear()
                create_gui()
                if exit_program_event.is_set():
                    break
                while not shutdown_event.is_set():
                    time.sleep(0.2)
                gui_closed = False
    except KeyboardInterrupt:
        print("\nCtrl+C pressed, stopping...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        shutdown_event.set()
        kb.unhook_all()
        print("Program exited.")
