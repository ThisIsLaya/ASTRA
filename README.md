# 🚀 ASTRA - Autonomous Spacecraft Telemetry & Risk Assistant
ASTRA is a Python project that simulates a spacecraft and monitors its condition using a Streamlit dashboard.

It generates spacecraft readings, detects problems, and displays alerts.

## How It Works

**1. Simulator (`simulator.py`)**
- Generates battery, oxygen, temperature, and communication readings.
- Simulates normal and emergency situations.

**2. Validator & Detector (`validator.py`, `detector.py`)**
- Checks if the data is valid.
- Detects problems in spacecraft readings.
- Classifies them as `NORMAL`, `WARNING`, or `CRITICAL`.

**3. Alerts (`alerts.py`)**
- Displays alerts when problems are found.
- Suggests possible actions.

**4. Dashboard (`main.py`)**
- Displays spacecraft readings and mission status.
- Allows users to change scenarios and update readings.
- Shows alerts and recommendations.

## Project Structure

```text
ASTRA/
├── simulator.py
├── validator.py
├── detector.py
├── alerts.py
├── main.py
└── README.md
```

## Technologies Used
- Python
- Streamlit

**Our goal:** Build a simple system that simulates spacecraft conditions and helps identify problems.
