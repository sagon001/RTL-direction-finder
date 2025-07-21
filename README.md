# RTL-SDR Drone Direction Finder

This project uses an RTL-SDR receiver on a Raspberry Pi mounted on a drone to detect and determine the direction of a signal at a specific frequency. Ideal for RF signal tracking, source localization, and spectrum scanning tasks.

## Features

- Signal scanning at target frequency
- Direction estimation based on signal strength and GPS
- Raspberry Pi + RTL-SDR integration
- Data logging for analysis

## Hardware Requirements

- Raspberry Pi 4 (or higher)
- RTL-SDR dongle
- Directional antenna (Yagi or patch)
- GPS module (for positioning)
- Drone platform (DJI/F450/etc.)
- Wireless module (for data acquisition to PC)
- Optional: IMU, magnetometer

## Software Stack

- Python 3.x
- `pyrtlsdr`
- `numpy`, `scipy`, `matplotlib`
- `gpsd` or similar for GPS data
- Optional: ROS or MAVLink

