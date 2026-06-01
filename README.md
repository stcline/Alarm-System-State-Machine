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

## Required Libraries

Before you begin it will be necessary to install the required libraries.

First run the following commands to update and upgrade the library sources:

```bash
sudo apt update
```

```bash 
sudo apt upgrade
```

Once those are set, you need to add the [Adafruit Circuitpython DHT Library](https://pypi.org/project/adafruit-circuitpython-dht/)
