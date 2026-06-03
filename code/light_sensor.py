# This script uses a Raspberry pi to read a photoresistor (light sensor) connected to an MCP3008 analog-to-digital converter and prints the light level as a percentage.
# The MCP3008 should be connected to the Raspberry Pi's SPI pins.
# The photoresistor should be connected as follows:
# - One leg of the photoresistor: Connect to 3.3V
# - The other leg of the photoresistor: Connect to CH1 on the MCP3008
import time
import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
# Create the SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# Create the chip select
cs = digitalio.DigitalInOut(board.D5)
# Create the MCP3008 object
mcp = MCP.MCP3008(spi, cs)
# Create an analog input channel on pin 1
light_channel = AnalogIn(mcp, MCP.P1)
try:
    while True:
        # Read the raw analog value from the photoresistor
        raw_value = light_channel.value

        # Convert the 16-bit scaled value to a percentage
        light_percent = (raw_value / 65535) * 100

        print(f"Light Level: {light_percent:.1f}%   Raw: {raw_value}   Voltage: {light_channel.voltage:.2f}V")

        # Wait before the next reading
        time.sleep(0.2)
except KeyboardInterrupt:
    print("Program stopped by User")
    