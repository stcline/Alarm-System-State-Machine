#This Python script uses a Raspberry Pi to read the state of a button connected to a GPIO pin and prints whether the button is pressed or not.
# The button (Keystudio Button Switch) should be connected to the Raspberry Pi's GPIO pins as follows:
# - One leg of the button: Connect to GPIO17 (Pin 11)
# - The other leg of the button: Connect to Ground

import time
import RPi.GPIO as GPIO # type: ignore

# Set the GPIO mode

GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the button
BUTTON_PIN = 17

# Set up the GPIO pin as an input with a pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
try:
    while True:
        # Read the state of the button
        button_state = GPIO.input(BUTTON_PIN)
        if button_state == GPIO.LOW:
            print("Button Pressed")
        else:
            print("Button Not Pressed")
        # Wait for 0.5 seconds before checking again
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Program stopped by User")
finally:    GPIO.cleanup() # Clean up GPIO settings