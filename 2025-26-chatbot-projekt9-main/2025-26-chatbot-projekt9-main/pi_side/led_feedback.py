from sense_hat import SenseHat
import sys
import time

sense = SenseHat()
sense.clear()

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

result = sys.argv[1] if len(sys.argv) > 1 else ""
score = sys.argv[2] if len(sys.argv) > 2 else None


check = [
    black, black, black, black, black, black, black, black,
    black, black, black, black, black, black, black, green,
    black, black, black, black, black, black, green, black,
    black, black, black, black, black, green, black, black,
    black, black, black, black, green, black, black, black,
    black, black, black, green, black, black, black, black,
    green, black, green, black, black, black, black, black,
    black, green, black, black, black, black, black, black,
]

cross = [
    red, black, black, black, black, black, black, red,
    black, red, black, black, black, black, red, black,
    black, black, red, black, black, red, black, black,
    black, black, black, red, red, black, black, black,
    black, black, black, red, red, black, black, black,
    black, black, red, black, black, red, black, black,
    black, red, black, black, black, black, red, black,
    red, black, black, black, black, black, black, red,
]

# A simple "S" or Arrow for Startup
startup_symbol = [
    black, black, blue,  blue,  blue,  blue,  black, black,
    black, blue,  black, black, black, black, blue,  black,
    black, blue,  black, black, black, black, black, black,
    black, black, blue,  blue,  blue,  black, black, black,
    black, black, black, black, black, blue,  black, black,
    black, blue,  black, black, black, blue,  black, black,
    black, black, blue,  blue,  blue,  black, black, black,
    black, black, black, black, black, black, black, black,
]

# A Question Mark for Trivia Start
trivia_start_symbol = [
    black, black, yellow, yellow, yellow, black, black, black,
    black, yellow, black, black, black, yellow, black, black,
    black, black, black, black, black, yellow, black, black,
    black, black, black, yellow, yellow, black, black, black,
    black, black, black, yellow, black, black, black, black,
    black, black, black, black, black, black, black, black,
    black, black, black, yellow, black, black, black, black,
    black, black, black, black, black, black, black, black,
]

# A simple "X" or door shape for Exit
exit_symbol = [
    red, red, red, red, red, red, red, red,
    red, black, black, black, black, black, black, red,
    red, black, black, black, black, black, black, red,
    red, red, red, black, black, red, red, red,
    red, black, black, black, black, black, black, red,
    red, black, black, black, black, black, black, red,
    red, red, red, red, red, red, red, red,
    black, black, black, black, black, black, black, black,
]

def set_optimal_orientation():
    # Get orientation data from the accelerometer
    acceleration = sense.get_accelerometer_raw()
    x = round(acceleration['x'], 0)
    y = round(acceleration['y'], 0)

    # Calculate rotation based on gravity
    if x == -1:
        sense.set_rotation(90)
    elif x == 1:
        sense.set_rotation(270)
    elif y == -1:
        sense.set_rotation(180)
    else:
        sense.set_rotation(0)
        
set_optimal_orientation()

if result == "startup":
    sense.set_pixels(startup_symbol)
elif result == "game_start":
    sense.set_pixels(trivia_start_symbol)
elif result == "game_exit":
    sense.set_pixels(exit_symbol)
elif result == "score":
    score_val = sys.argv[2] if len(sys.argv) > 2 else "0"
    sense.show_message(score_val, text_colour=yellow)
elif result == "correct":
    sense.set_pixels(check)
elif result == "wrong":
    sense.set_pixels(cross)

time.sleep(1.5)
sense.clear()

