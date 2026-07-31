import time
import random
from sense_hat import SenseHat

sense = SenseHat()

def run_haptic_game():
    sense.clear()
    
    # 1. Introductory Message
    target_seconds = random.randint(1, 20)
    sense.show_message(f"Goal: {target_seconds}s", scroll_speed=0.05, text_colour=(0, 255, 255))
    
    # Wait for the user to press the joystick to START the timer
    # We wait up to 40 seconds for the first press
    start_event = sense.stick.wait_for_event(emptybuffer=True)
    if start_event.action != "pressed":
        return # Resume normal operation if no press

    start_time = time.time()
    print(f"Timer started! Aiming for {target_seconds} seconds.")

    # 2. Wait for the user to press again to STOP the timer
    # If they don't press within 40 seconds, we auto-exit
    end_event = None
    timeout = 40
    start_wait = time.time()
    
    while (time.time() - start_wait) < timeout:
        end_event = sense.stick.wait_for_event(emptybuffer=False)
        if end_event.action == "pressed":
            break
    
    if not end_event or (time.time() - start_wait) >= timeout:
        sense.show_message("Timeout", text_colour=(255, 0, 0))
        return

    end_time = time.time()
    
    # 3. Calculate the difference
    actual_duration = end_time - start_time
    diff_ms = abs(int((actual_duration - target_seconds) * 1000))
    
    # 4. Display result
    # Green if close (< 500ms), Red if far
    color = (0, 255, 0) if diff_ms < 500 else (255, 0, 0)
    sense.show_message(f"Off by {diff_ms}ms", text_colour=color)
    
    sense.clear()
    
if __name__ == "__main__":
    # This allows the script to be run directly via SSH
    run_haptic_game()