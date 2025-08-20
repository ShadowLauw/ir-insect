# IR-Insect

IR-Insect is a Raspberry Pi project for detecting insects in a scanned area.  
The setup is designed to be mounted on a moving platform, such as a drone, to monitor insects in real time.  
We use 3D-printed insects with *catadioptric* material to simulate reflections.  
An IR LED is placed very close to the camera so that reflections off the insects are captured correctly.  
The camera and LED must be aimed directly at the insects to ensure the reflected IR light reaches the camera.  
The Tkinter GUI allows real-time monitoring while OpenCV handles image processing.

---

## Hardware Requirements

- Raspberry Pi 4 (or compatible)  
- MicroSD card (8GB+)  
- Raspberry Pi NoIR camera   
- IR LED & Filter for its wavelength

---

## OS Installation

1. Download **Raspberry Pi Imager**: [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)  
2. Install the **Raspberry Pi OS (64-bit)** to the SD card.  
3. Boot the Pi.

---

## Hardware Setup

- Connect the camera to the Raspberry Pi camera port.  
- Place the IR LED **right next to the camera** and point both directly at the insects.  
- Position 3D-printed insects with *catadioptric* surfaces in the camera’s field of view.    
- Connect any GPIO-controlled devices if needed (Pin 18 by default; can be changed in the code).  

---

## Project Setup with UV

```bash
python3 -m pip install --user uv
git clone git@github.com:ShadowLauw/ir-insect.git
cd ir-insect
uv sync
source .venv/bin/activate
sudo apt update
sudo apt install build-essential python3-dev libcap-dev python3-picamera2 fonts-noto-color-emoji
```

> **Note:** Picamera2 relies on the system’s libcamera stack.  
> To use it in a virtual environment, create the venv with `--system-site-packages` so that Picamera2 and libcamera are accessible:
```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
```
---

## Running the Project

```bash
source .venv/bin/activate
uv run python main.py
```

--- 
## Development Tools

```bash
black --check .
ruff check .
```