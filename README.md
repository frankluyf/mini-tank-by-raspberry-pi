# mini-tank-by-raspberry-pie
The tank is built up of a gun which could change it's angle in about 60 degrees in different dimensions and is controlled by raspberry pie 5. The four wheels are Mecanum wheel so they can move in horizontal directions. A web page and it's server is built on raspberry pie to control it under the same wifi.


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

## 🔌 Wiring Diagram

A clear wiring diagram is crucial for replicating this project.

*(Insert an image of your wiring diagram here. You can create one using tools like Fritzing or draw.io and place the image file in a `docs/images` folder.)*

**`[docs/images/wiring_diagram.png]`**

---

## 💻 Software & Setup

### Prerequisites

* Raspberry Pi OS (Bookworm or newer) flashed onto a MicroSD card.
* Python 3.11+
* Git

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Install required Python libraries:**
    This project uses the following key libraries. Install them using `pip`.
    ```bash
    pip install -r requirements.txt
    ```
    *Your `requirements.txt` file should include libraries like `flask`, `gpiozero`, etc.*

3.  **Configure Wi-Fi:**
    Ensure your Raspberry Pi is connected to the same Wi-Fi network that you will use for control.

---

## 🚀 How to Use

1.  **Start the web server:**
    Navigate to the project directory and run the main application script.
    ```bash
    python src/main.py
    ```

2.  **Find the Raspberry Pi's IP Address:**
    In the terminal, type:
    ```bash
    hostname -I
    ```

3.  **Access the Control Interface:**
    Open a web browser on your phone or computer (on the same Wi-Fi network) and navigate to `http://<YOUR_PI_IP_ADDRESS>:5000`.

4.  **Control the Rover:**
    Use the on-screen controls to move the rover and operate the water cannon.

---

## 📂 Project Structure
