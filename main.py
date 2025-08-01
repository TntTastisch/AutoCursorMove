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
        "name": "Small random movement",
        "func": lambda: (rdm.randint(-100, 100), rdm.randint(-100, 100)),
    },
    {
        "name": "Large random movement",
        "func": lambda: (rdm.randint(-300, 300), rdm.randint(-300, 300)),
    },
    {"name": "Horizontal movement", "func": lambda: (rdm.randint(-150, 150), 0)},
    {"name": "Vertical movement", "func": lambda: (0, rdm.randint(-150, 150))},
    {
        "name": "Diagonal jumps",
        "func": lambda: (rdm.choice([-200, 200]), rdm.choice([-200, 200])),
    },
    {
        "name": "Trembling in place",
        "func": lambda: (rdm.randint(-15, 15), rdm.randint(-15, 15)),
    },
    {"name": "No movement (pause)", "func": lambda: (0, 0)},
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
        duration = rdm.uniform(0.4, 1.2)
        gui.moveTo(target_x, target_y, duration=duration, tween=gui.easeInOutQuad)
    except Exception as e:
        print(f"Error during movement: {e}")
        reset_cursor_position()


def move_cursor_loop():
    print("Mouse movement loop started (ESC to exit)")
    while not shutdown_event.is_set():
        try:
            if not is_cursor_in_bounds(*gui.position()):
                reset_cursor_position()
            random_move_cursor()
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


def create_gui():
    global gui_closed
    gui_closed = False
    root = tk.Tk()
    root.title("Mausbewegungs-Muster")
    root.geometry("400x450")
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
    try:
        print(f"Screen size: {screen_width}x{screen_height}")
        while not exit_program_event.is_set():
            shutdown_event.clear()
            create_gui()
            if exit_program_event.is_set():
                break
            while not shutdown_event.is_set():
                time.sleep(0.2)
            gui_closed = False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        shutdown_event.set()
        kb.unhook_all()
        print("Program exited.")
