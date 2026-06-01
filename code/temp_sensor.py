#This Python script uses a Raspberry Pi to read the temperature from a DHT11 sensor and print the temperature in Celsius.
# The DHT11 sensor should be connected to the Raspberry Pi's GPIO pins as follows:
# - VCC: Connect to 3.3V
# - DATA: Connect to GPIO4 (Pin 7)
# - GND: Connect to Ground
# - If using a bare 4-pin DHT11, add a 4.7k to 10k pull-up resistor between VCC and DATA

import time
import board
import adafruit_dht

# Set up the DHT11 sensor on GPIO4
dht_device = adafruit_dht.DHT11(board.D4)

try:
    while True:
        try:
            # Read the temperature in Celsius
            temperature_c = dht_device.temperature

            if temperature_c is not None:
                print(f"Temperature: {temperature_c:.1f} C")
            else:
                print("No reading received")

        except RuntimeError as error:
            print(f"Read error: {error}")

        # Wait for 2 seconds before checking again
        time.sleep(2.0)

except KeyboardInterrupt:
    print("Program stopped by User")

finally:
    dht_device.exit()  # Clean up the sensor settings