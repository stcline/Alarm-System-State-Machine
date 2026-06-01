# This Python script uses a Raspberry Pi to read distance data from an ultrasonic sensor (HC-SR04) and prints the distance in centimeters.
# The sensor should be connected to the Raspberry Pi's GPIO pins as follows:
# - VCC: Connect to 5V
# - GND: Connect to Ground
# - Trig: Connect to GPIO23 (Pin 16)
# - Echo: Connect to GPIO24 (Pin 18)

import time
import RPi.GPIO as GPIO # type: ignore

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for the ultrasonic sensor
TRIG = 23
ECHO = 24

# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        # Send a 10 microsecond pulse to trigger the sensor
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        # Wait for the echo to start
        while GPIO.input(ECHO) == 0:
            pass
        pulse_start = time.time()
        # Wait for the echo to end
        while GPIO.input(ECHO) == 1:
            pass
        pulse_end = time.time()
        # Calculate the duration of the pulse
        pulse_duration = pulse_end - pulse_start
        # Calculate the distance in centimeters (speed of sound is 34300 cm/s)
        distance = pulse_duration * 17150
        print(f'Distance: {distance:.2f} cm')
        # Wait for 1 second before the next reading
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by User")
finally:    GPIO.cleanup() # Clean up GPIO settings
