# This Python script uses a Raspberry Pi with an MCP3008 analog-to-digital converter
# to read the sound level from a Keystudio analog sound sensor and print the sound level as a percentage.
# The MCP3008 should be connected to the Raspberry Pi's SPI pins.
# The sound sensor should be connected as follows:
# - VCC: Connect to 3.3V
# - GND: Connect to Ground
# - S: Connect to CH0 on the MCP3008

import time
import board
import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Create the SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the chip select
cs = digitalio.DigitalInOut(board.CEO)

# Create the MCP3008 object
mcp = MCP.MCP3008(spi, cs)

# Create an analog input channel on pin 0
sound_channel = AnalogIn(mcp, MCP.P0)

try:
    while True:
        # Read the raw analog value from the sound sensor
        raw_value = sound_channel.value

        # Convert the 16-bit scaled value to a percentage
        sound_percent = (raw_value / 65535) * 100

        print(f"Sound Level: {sound_percent:.1f}%   Raw: {raw_value}   Voltage: {sound_channel.voltage:.2f}V")

        # Wait before the next reading
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Program stopped by User")