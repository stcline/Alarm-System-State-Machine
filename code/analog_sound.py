# This Python script uses a Raspberry Pi to sense sound using a Keystudio analog sound sensor and prints the sound level as a percentage.
# The sensor should be connected to the Raspberry Pi's GPIO pins as follows:
# - VCC: Connect to 5V
# - GND: Connect to Ground
# - OUT: Connect to GPIO18 (Pin 12) for analog output

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
        # Read the sound level from the sensor
        sound_level = GPIO.input(SOUND_PIN)
        # Print the sound level as a percentage (0% for LOW, 100% for HIGH)
        if sound_level == GPIO.HIGH:
            print("Sound Level: 100%")
        else:
            print("Sound Level: 0%")
        # Wait for 1 second before the next reading
        time.sleep(1)
except KeyboardInterrupt:
    print("Program stopped by User")
finally:    GPIO.cleanup() # Clean up GPIO settings
