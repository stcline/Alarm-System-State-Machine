# This Python script uses a Raspberry Pi to read temperature data from a DHT11 sensor and prints the temperature in Celsius.
# The sensor should be connected to the Raspberry Pi's GPIO pins, and the necessary kernel modules must be loaded for the 1-Wire interface to work.
# Pins used are as follows:
# - VCC: Connect to 3.3V    
# - GND: Connect to Ground
# - Data: Connect to GPIO4 (Pin 7) with a 4.7kΩ pull-up resistor between the Data line and VCC

# dht11_temp.py
import time
import board
import adafruit_dht

# DHT11 connected to GPIO4 (physical pin 7)
dht_device = adafruit_dht.DHT11(board.D4)

try:
    while True:
        try:
            temperature_c = dht_device.temperature
            if temperature_c is not None:
                print(f"Temperature: {temperature_c:.1f} C")
            else:
                print("No reading received")
        except RuntimeError as error:
            # DHT sensors often fail transiently; just retry
            print(f"Read error: {error}")
        time.sleep(2.0)
finally:
    dht_device.exit()