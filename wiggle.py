import subprocess
import time
import re
import pyautogui
import random

def get_idle_time():
    """Gets the system idle time using ioreg."""
    try:
        process = subprocess.run(['ioreg', '-c', 'IOHIDSystem'], capture_output=True, text=True, check=True)
        output = process.stdout
        match = re.search(r'"HIDIdleTime" = (\d+)', output)
        if match:
            idle_time_ns = int(match.group(1))  # Nanoseconds
            return idle_time_ns / 10**9  # Convert to seconds
        else:
            return 0
    except subprocess.CalledProcessError as e:
        print(f"Error running ioreg: {e}")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 0

def is_idle(threshold_seconds=60):
    idle_time = get_idle_time()
    return idle_time > threshold_seconds

def nudge_mouse():
    """Moves the mouse slightly in a random direction."""
    try:
        current_x, current_y = pyautogui.position()
        # Generate a small random offset.
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        new_x = current_x + offset_x
        new_y = current_y + offset_y
        # Keep the mouse within screen boundary.
        screen_width, screen_height = pyautogui.size()
        new_x = max(0, min(new_x, screen_width - 1)) 
        new_y = max(0, min(new_y, screen_height - 1))
        pyautogui.moveTo(new_x, new_y)
        print("Mouse nudged.")
    except Exception as e:
        print(f"Error nudging mouse: {e}")

if __name__ == "__main__":
    try:
        while True:
            idle_time = get_idle_time()
            if is_idle(45):  # Check if idle for X seconds (adjust as needed)
                print("System is idle. Nudging mouse.")
                nudge_mouse()
            time.sleep(5)  # Check every 5 seconds (adjust as needed)
    except KeyboardInterrupt:
        print("Script stopped by user.")
