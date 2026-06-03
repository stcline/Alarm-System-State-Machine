# This Python script uses a Raspberry Pi to create an alarm system.  It activates the system when a button is pressed and deactivates it when the button is pressed again.  When the system is active, it prints "Alarm Activated!" every second.
# The button (Keystudio Button Switch) should be connected to the Raspberry Pi's GPIO pins as follows:
# - One leg of the button: Connect to GPIO17 (Pin 11)
# - The other leg of the button: Connect to Ground
# Pressing the button will toggle the alarm state between active and inactive.
# Once activated the system will use the following three sensors to monitor the environment:
# 1. Sound Sensor (Keystudio Analog Sound Sensor) connected to MCP3008 channel 0
# 2. Temperature Sensor (DHT11) connected to GPIO4 (Pin 7)
# 3. Distance Sensor (HC-SR04) connected to GPIO23 (Pin 16) and GPIO24 (Pin 18)
# When any of those sensors detect a value above a certain threshold, the system will print "ALERT: Sensor Triggered!" and the current readings from all three sensors.

import time
import board
import busio
import digitalio
import adafruit_dht
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO # type: ignore

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
BUTTON_PIN = 17
TRIG_PIN = 23
ECHO_PIN = 24

# Set up button and ultrasonic sensor pins
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.output(TRIG_PIN, False)

# Give the ultrasonic sensor time to settle
time.sleep(2)

# Set up the DHT11 temperature sensor
dht_device = adafruit_dht.DHT11(board.D4)

# Set up SPI and MCP3008 for the analog sound sensor
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE0)
mcp = MCP.MCP3008(spi, cs)
sound_channel = AnalogIn(mcp, MCP.P0)

# Alarm state
alarm_active = False
last_button_state = GPIO.HIGH

# Thresholds
SOUND_THRESHOLD = 12.0
TEMP_THRESHOLD = 30.0
DISTANCE_THRESHOLD = 20.0

def read_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    pulse_start = time.time()
    pulse_end = time.time()

    timeout = time.time() + 0.05
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if time.time() > timeout:
            return None

    timeout = time.time() + 0.05
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if time.time() > timeout:
            return None

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2
    return distance

try:
    while True:
        # Read the button state
        button_state = GPIO.input(BUTTON_PIN)

        # Toggle alarm state on button press
        if button_state == GPIO.LOW and last_button_state == GPIO.HIGH:
            alarm_active = not alarm_active
            time.sleep(0.3)

        last_button_state = button_state

        # Read sound level from MCP3008 channel 0
        sound_percent = (sound_channel.value / 65535) * 100

        # Read temperature from DHT11
        try:
            temperature_c = dht_device.temperature
        except RuntimeError:
            temperature_c = None

        # Read distance from HC-SR04
        distance_cm = read_distance()

        # Format display text
        alarm_status = "Armed" if alarm_active else "Disarmed"
        sound_text = f"{sound_percent:.1f}%"
        temp_text = f"{temperature_c:.1f} C" if temperature_c is not None else "N/A"
        distance_text = f"{distance_cm:.1f} cm" if distance_cm is not None else "N/A"

        # Print one complete status line
        print(f"Alarm Status: {alarm_status} | Sound: {sound_text} | Temperature: {temp_text} | Distance: {distance_text}")

        # Check thresholds only when alarm is armed
        if alarm_active:
            sound_triggered = sound_percent > SOUND_THRESHOLD
            temp_triggered = temperature_c is not None and temperature_c > TEMP_THRESHOLD
            distance_triggered = distance_cm is not None and distance_cm < DISTANCE_THRESHOLD

            if sound_triggered or temp_triggered or distance_triggered:
                print("ALERT: Sensor Triggered!")

        time.sleep(.3)

except KeyboardInterrupt:
    print("Program stopped by User")

finally:
    GPIO.cleanup()
    dht_device.exit()