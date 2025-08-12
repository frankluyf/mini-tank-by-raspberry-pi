# mini-tank-by-raspberry-pi
The tank is built up of a gun which could change it's angle in about 60 degrees in different dimensions and is controlled by raspberry pie 5. The four wheels are Mecanum wheel so they can move in horizontal directions. A web page and it's server is built on raspberry pie to control it under the same wifi.

![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue)

## Overview

This project is a remote-controlled rover built with a **Raspberry Pi 5**. It features four **Mecanum wheels** that allow for omnidirectional movement, including horizontal strafing. The rover is equipped with a water cannon mounted on a 2-axis gimbal, allowing its angle to be adjusted up to 60 degrees for precise aiming.

Control is handled via a self-hosted web interface, allowing any device on the same Wi-Fi network to operate the rover through a browser.

---

<img src="photos/tank_gif1.gif" alt="Project Demo GIF" width="500">

## ✨ Key Features

* **Omni-Directional Movement**: Utilizes Mecanum wheels to move forward, backward, sideways, and rotate on the spot.
* **Adjustable Water Cannon**: A 2-axis gimbal provides a 60-degree range of motion for aiming.
* **Web-Based Control**: A responsive web interface hosted on the Raspberry Pi for intuitive control from a phone or computer.
* **Real-time Commands**: Low-latency control over Wi-Fi.
* **Powered by Raspberry Pi 5**: Leverages the performance of the latest Raspberry Pi for smooth operation.
* **Camera to transmit live videos**: A panorama camera that can transmit live videos to the local website
* **Connection to loudspeaker**: Connects to a Bluetooth loudspeaker which can send live recordings to the car and implement the function of remote communication.
---

## 🛠️ Hardware Components

| Component | Quantity | Notes |
| :--- | :--- | :--- |
| Raspberry Pi 5 | 1 | The brain of the rover. |
| Mecanum Wheels | 4 | For omnidirectional movement. |
| DC Geared Motors | 4 | To drive the wheels. |
| Motor Driver | 1 | L298N with 8 IN and 8 OUT pins |
| Micro Servos | 2 | For the 2-axis gun turret (pan/tilt). |
| high voltage Gun | 1 | For the water cannon. |
| Power Source | 2 | A powerful powerbank for the gun and a rather small powerbank for the Raspberry pie|
| MicroSD Card | 1 | 128GB or larger, for the Raspberry. |
| Jumper Wires | Various | For connecting components. |
| Chassis/Frame | 1 | To mount all the components. |

---

## 🔌 Robot Structure (Simplified Diagram)

This is a simplified side view representation of the robot's three-layer structure:

<pre>
        _________________
       /                 \  &lt;-- Top Layer Divider
      |      _______      |
      |     /       \     |  &lt;-- Gun
      |    |  Laser  |    |
      |    \_______/    |
^     |       O         |  &lt;-- LED
|     |      -----      |
|     |     |Gimbal|     |
|     |      -----      |
      \_________________/

        -----------------
       /                 \  &lt;-- Middle Layer Divider
      |  -------         |
      | | L298N |        |  &lt;-- L298N, Power Bank [PB]
      |  -------         |
      |  -----    -----  |
      |  | [PB]  | RPi   |  &lt;-- Raspberry Pi [RPi]
      |  -----    -----  |
      \-----------------/

        =================
       /                 \  &lt;-- Bottom Layer
      |  ---------      |
      | | Big Batt|      |
      |  ---------      |
      |     ---          |
      |    |Relay|       |  &lt;-- Relay
      |     ---       |
      \=================/

          O   O   O   O      &lt;-- Wheels (Very Simplified)
</pre>

**Top Layer:** Contains the gimbal in the center, the gun mounted on top of it, a laser emitter at the gun's muzzle, an LED at the base of the gun barrel, and the camera positioned in front of the (fake) scope.

**Middle Layer:** Houses the L298N motor driver in the front, a power bank on the left rear, and the Raspberry Pi on the right rear.

**Bottom Layer:** Contains the large battery for powering the motors and the gun mechanism, located at the front of the chassis. A small relay is positioned slightly behind the battery.

**Note:** This is a highly simplified representation and does not show the exact placement or connections of all components.


## 💻 Software & Setup

### Prerequisites

* Raspberry Pi OS (Bookworm or newer) flashed onto a MicroSD card.
* Python 3.11+
* Git
* Visual Studio Code (highly recommended)

### Installation

Follow these steps to set up the project environment on your Raspberry Pi.

1.  **Clone the Repository**

    First, download the project files from GitHub to your Raspberry Pi and navigate into the newly created directory.

    ```bash
    git clone https://github.com/frankluyf/mini-tank-by-raspberry-pi.git
    cd mini-tank-by-raspberry-pi
    ```

2.  **Create and Activate a Virtual Environment**

    Using a virtual environment is highly recommended to keep project dependencies isolated from the system's global Python packages.

    ```bash
    # Create a virtual environment named "tank_venv"
    cd tank
    # Recommend to install the environment in tank 
    python3 -m venv tank_venv

    # Activate the virtual environment
    source tank_venv/bin/activate
    ```
    *(You'll know it's active when you see `(tank_venv)` at the beginning of your command prompt.)*

3.  **Install Required Libraries**

    With the virtual environment active, install all the necessary Python libraries using the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Wi-Fi**

    Ensure your Raspberry Pi is connected to the same Wi-Fi network that you will use to control the vehicle.

After these steps, the software environment is fully configured and ready to run.

---

## 🚀 How to Use

1.  **Connect to Raspberry:**
    Contact to raspberry pi using Visual Studio Code

2.  **Activate environment:**
    In the terminal, type:
    ```bash
    cd tank
    source tank_env/bin/activate
    ```

3.  **Activate web server**
    in the terminal, type:
    ```bash
    cd servo_web
    ./test.sh
    python server.py
    ```
    
5.  **Activate web page**
    in another terminal, type:
    ```bash
    cd tank/servo_web
    ./start.sh
    ```

---

## 📂 Project Structure



## 🗒️Hardware Connection Table

This document details the hardware wiring for all modules in this project. Please follow this guide carefully during assembly to ensure all connections are correct.

### Main Control & Peripherals

| Source Module & Port | Destination & Connection | Raspberry Pi Pin | Function / Description |
| :--- | :--- | :--- | :--- |
| **Relay** |
| Relay `S` (Signal) | -> Raspberry Pi GPIO | **Pin 15** (GPIO22) | Main power control signal |
| Relay `+` (VCC) | -> Raspberry Pi 5V | **Pin 2** (5V) | Power for the relay module |
| Relay `-` (GND) | -> Raspberry Pi GND | **Pin 39** (GND) | Ground for the relay module |
| **Motor Driver (L298N)** |
| L298N `IN1` | -> Raspberry Pi GPIO | **Pin 11** (GPIO17) | Motor A Control |
| L298N `IN2` | -> Raspberry Pi GPIO | **Pin 13** (GPIO27) | Motor A Control |
| L298N `IN3` | -> Raspberry Pi GPIO | **Pin 16** (GPIO23) | Motor B Control |
| L298N `IN4` | -> Raspberry Pi GPIO | **Pin 18** (GPIO24) | Motor B Control |
| L298N `IN5` | -> Raspberry Pi GPIO | **Pin 29** (GPIO5) | Motor C Control |
| L298N `IN6` | -> Raspberry Pi GPIO | **Pin 31** (GPIO6) | Motor C Control |
| L298N `IN7` | -> Raspberry Pi GPIO | **Pin 36** (GPIO16) | Motor D Control |
| L298N `IN8` | -> Raspberry Pi GPIO | **Pin 37** (GPIO26) | Motor D Control |
| **Camera** |
| Camera `USB` Connector | -> Raspberry Pi USB Port | Any USB Port | Video Data Capture |

<br>

### Power System

| Source / Junction Point | Destination & Connection | Function / Description |
| :--- | :--- | :--- |
| L298N `GND` | -> Raspberry Pi `GND` (e.g., Pin 9)<br>-> Relay `NC`<br>-> Battery `Negative (-)` | **System Main Ground Junction.** All grounds are tied together at this point. |
| L298N `VCC` (+12V) | -> Relay `NO`<br>-> Battery `Positive (+)` | **System Main Power Junction.** All positive leads are tied together at this point. |
| Relay `COM` | -> "Gun" Module `Negative (-)` | **Switched Output.** Controlled by the relay. |
| Relay `NC` | -> "Gun" Module `Positive (+)`<br>   *(Also connected to Ground)* | **Default Output.** Connected to ground by default. |


> ### ⚠️ **Important Wiring Warning**
> **Please double-check your circuit diagram and logic before applying power to prevent potential damage to your components.** Standard practice is typically to use a relay to switch a single positive (+) power line.

