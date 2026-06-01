# This Python script uses a Raspberry Pi to detect sound using a Keystudio sound sensor and prints whether sound is detected.
# The sensor should be connected to the Raspberry Pi's GPIO pins as follows:
# - VCC: Connect to 3.3V
# - GND: Connect to Ground
# - DO: Connect to GPIO18 (Pin 12) for digital threshold output
# - Adjust the potentiometer on the module to set the sound detection threshold

import time
import RPi.GPIO as GPIO # type: ignore

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the sound sensor
SOUND_PIN = 18

# Set up the GPIO pin as an input
GPIO.setup(SOUND_PIN, GPIO.IN)

try:
    while True:
        # Read the state of the sound sensor
        sound_state = GPIO.input(SOUND_PIN)

        # Many sound sensor modules output LOW when sound exceeds the threshold
        if sound_state == GPIO.LOW:
            print("Sound Detected")
        else:
            print("No Sound Detected")

        # Wait before the next reading
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by User")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
