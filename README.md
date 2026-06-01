# Intruder Alert System

This project is an intruder alert device built with a Raspberry Pi 3B, 4B, or 5B, a button, an HC-SR04 ultrasonic sensor, a temperature/humidity sensor, and a sound sensor. The system uses these inputs to detect nearby motion, unusual sound, and environmental changes, then warns the user when an intruder may be present.  

## Project Overview

The goal of the system is to monitor its surroundings and alert the user when certain sensor conditions are detected. The system uses a button for activation and deactivation, an HC-SR04 ultrasonic sensor to detect nearby objects, a sound sensor to detect loud noise, and a temperature/humidity sensor to detect environmental changes that may indicate disturbance in the area.  

The system communicates its status through the screen and LEDs. The screen displays messages to show the current state, one LED indicates that the system is active, and another LED indicates that an intruder has been detected.  

## Inputs

The intruder alert system uses the following inputs:

- Button to activate or deactivate the system.  
- HC-SR04 ultrasonic sensor to detect when an object moves close to the system.  
- Sound sensor to detect significantly loud sound.  
- Temperature/humidity sensor to detect unusual environmental changes such as a sudden change in temperature or humidity.  

## Outputs

The system uses the following outputs:

- Screen messages such as `IDLE`, `ACTIVE`, and `ALARM`.  
- A green LED to show that the system is active.  
- A red LED to show that an intruder has been detected.  

## State Machine

<img width="504" height="672" alt="State_Diagram_Alarm" src="https://github.com/user-attachments/assets/d0befad9-4de5-44a4-bfa6-946a5d365ab1" />

The system is modeled with three states: `IDLE`, `ACTIVE`, and `ALARM`. In the `IDLE` state, the system is waiting to be activated. In the `ACTIVE` state, the system monitors the sensors for possible intruder conditions. In the `ALARM` state, the system signals that an intruder has been detected.  

### State Transitions

- `IDLE` stays in `IDLE` when there is no input (`NI`).  
- `IDLE` changes to `ACTIVE` when the user activates the system (`A`).  
- `ACTIVE` returns to `IDLE` when the user deactivates the system (`D`).  
- `ACTIVE` remains in `ACTIVE` when the object is far, the environment is within normal temperature/humidity range, and the sound is quiet.  
- `ACTIVE` changes to `ALARM` when any alert condition is detected, such as object close, unusual temperature/humidity readings, or loud sound.  
- `ALARM` remains in `ALARM` while any alarm condition continues to exist.  

## Program Behavior

The program begins in the `IDLE` state and displays `IDLE` on the screen. A variable is used to track whether the system is active, allowing the button to toggle the system between `IDLE` and `ACTIVE`.  

When the system is active, the program continuously checks sensor values inside the main loop. If the HC-SR04 ultrasonic sensor detects a close object, the sound sensor detects a loud sound, or the temperature/humidity sensor detects unusual environmental conditions, the program turns on the red LED and displays `ALARM`. Otherwise, it keeps the system in the `ACTIVE` state and displays `ACTIVE`.  

## Installing Libraries and Dependencies

These Python scripts were written for a Raspberry Pi running Raspberry Pi OS with Python 3.

Because newer Raspberry Pi OS releases use an externally managed Python environment, it is recommended to install Python packages inside a virtual environment instead of using `pip3` system-wide.   

### 1. Update the Pi

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Install system packages

These packages provide Python venv support and GPIO-related dependencies used by CircuitPython/Blinka on Raspberry Pi.  

```bash
sudo apt-get install -y python3-full python3-venv i2c-tools libgpiod-dev python3-libgpiod python3-rpi.gpio
```

### 3. Create and activate a virtual environment

```bash
python3 -m venv ~/sensor-env
source ~/sensor-env/bin/activate
```

After activation, your terminal prompt should show the virtual environment name.  
You must activate this environment each time before running the DHT11 or MCP3008 scripts.   

### 4. Upgrade pip inside the virtual environment

```bash
pip install --upgrade pip
```

### 5. Install Python libraries

Install the libraries needed for all of the scripts:

```bash
pip install adafruit-blinka
pip install adafruit-circuitpython-dht
pip install adafruit-circuitpython-mcp3xxx
```

#### What each library is for

- `python3-rpi.gpio`  
  Used by scripts that directly use the `RPi.GPIO` library, such as the button script.  

- `adafruit-blinka`  
  Provides CircuitPython-compatible modules such as `board`, `busio`, and `digitalio` on Raspberry Pi Linux.   

- `adafruit-circuitpython-dht`  
  Used for reading the DHT11 temperature sensor.   

- `adafruit-circuitpython-mcp3xxx`  
  Used for reading analog sensors through an MCP3008 ADC, including the Keystudio analog sound sensor.   

### 6. Enable SPI for the MCP3008

The MCP3008 uses the Raspberry Pi SPI interface, so SPI must be enabled before running the analog sound sensor script. Adafruit’s MCP3008 Raspberry Pi examples use the hardware SPI pins.   

Enable SPI with:

```bash
sudo raspi-config
```

Then go to:

```text
Interface Options -> SPI -> Yes
```

Reboot the Pi after enabling SPI:

```bash
sudo reboot
```

### 7. Running the scripts

#### Button script

If your button script uses `RPi.GPIO`, it can usually be run with:

```bash
python3 button.py
```

#### DHT11 temperature script

Activate the virtual environment first:

```bash
source ~/sensor-env/bin/activate
python3 dht11_temp.py
```

#### MCP3008 + analog sound sensor script

Activate the virtual environment first:

```bash
source ~/sensor-env/bin/activate
python3 analog_sound_mcp3008.py
```

### 8. Common issues

#### `error: externally-managed-environment`

This means Raspberry Pi OS is blocking system-wide `pip` installs.  
Use a virtual environment as shown above instead of `sudo pip3 install ...`.   

#### `ModuleNotFoundError: No module named 'board'`

This usually means `adafruit-blinka` is not installed in the active virtual environment.   

#### `DHT sensor not found, check wiring`

This is usually caused by incorrect wiring, a missing pull-up resistor on a bare DHT11 sensor, or a bad sensor. The DHT CircuitPython guide documents the library setup, while the Raspberry Pi DHT wiring guide uses GPIO4 in its examples.   

#### MCP3008 not responding

Make sure SPI is enabled and that the MCP3008 is wired to the Pi’s hardware SPI pins correctly. The Raspberry Pi MCP3008 examples use SPI with `board.SCK`, `board.MISO`, and `board.MOSI`.   
