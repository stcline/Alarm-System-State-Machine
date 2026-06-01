# This Python script uses a Raspberry Pi to read temperature data from a DHT11 sensor and prints the temperature in Celsius.
# The sensor should be connected to the Raspberry Pi's GPIO pins, and the necessary kernel modules must be loaded for the 1-Wire interface to work.
# Pins used are as follows:
# - VCC: Connect to 3.3V    
# - GND: Connect to Ground
# - Data: Connect to GPIO4 (Pin 7) with a 4.7kΩ pull-up resistor between the Data line and VCC

import time
import adafruit_dht 

# Set the sensor GPIO pin number
PIN = 4

# Create an instance of the DHT11 sensor
dht_device = adafruit_dht.DHT11(PIN)

while True:
    # Read the humidity and temperature from the sensor
    humidity, temperature = dht_device.read_retry()
    if humidity is not None and temperature is not None:
        print(f'Temperature: {temperature:.1f}°C  Humidity: {humidity:.1f}%')
    else:
        print('Failed to get reading. Try again!')
    # Wait for 2 seconds before the next reading
    time.sleep(2)