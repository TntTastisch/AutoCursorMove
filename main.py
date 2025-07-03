import time
import random as rdm
import pyautogui as gui
import keyboard as kb

running = True
screen_width, screen_height = gui.size()

def on_event(event):
    global running
    if event.name == 'esc':
        print("Shutting down")
        running = False


def random_move_cursor():
    try:
        global screen_width, screen_height
        max_x = int(screen_width / 4)
        max_y = int(screen_height / 4)
        move_x = rdm.randint(-max_x, max_x)
        move_y = rdm.randint(-max_y, max_y)
        print(f"Moving cursor by ({move_x}, {move_y})")
        gui.moveRel(move_x, move_y, duration=0.5)
    except Exception:
        random_move_cursor()


def move_cursor():
    while running:
        time.sleep(1)
        print("Moving cursor...")
        random_move_cursor()
        print("Moving cursor done.")

if __name__ == "__main__":
    kb.on_press(on_event)
    try:
        move_cursor()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        exit(-1)
