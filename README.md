# 🚀 ASTRA — Autonomous Spacecraft Telemetry & Risk Assistant
**What if a spacecraft developed a problem millions of kilometres away from Earth? How would mission operators know something was wrong?**

That's the idea behind **ASTRA** — a Python-based spacecraft monitoring prototype designed to simulate mission conditions, identify potential system failures, and help operators understand what needs attention.

Built using **Python and Streamlit**, ASTRA brings together simulated spacecraft data, data validation, anomaly detection, and an interactive mission control dashboard.

Instead of simply displaying sensor readings, ASTRA takes those readings through a series of checks to highlight unusual conditions, prioritize important alerts, and suggest possible responses.

## 🛰️ How ASTRA Works

ASTRA is made up of four connected components. Each handles a different part of the monitoring process.

### 1. Telemetry Simulator (`simulator.py`) — Bringing the Spacecraft to Life

Every mission starts with data. Since we aren't connected to a real spacecraft, we built a simulator that acts as our virtual spacecraft.

It generates changing readings for:

- **Battery:** Available power
- **Oxygen:** Remaining oxygen level
- **Temperature:** Cabin temperature
- **Communication:** Connection status
- **Timestamp:** When the latest reading was recorded

The simulator supports different mission scenarios, including normal operation, battery emergencies, oxygen problems, temperature anomalies, and communication loss.

### 2. Data Validation & Anomaly Detection (`validator.py`, `detector.py`) — Making Sense of the Data

Not every incoming reading should automatically be trusted. Before identifying problems, ASTRA checks whether the data is complete and valid.

- **`validator.py`** checks required fields, data types, missing values, and acceptable sensor ranges.
- **`detector.py`** compares valid readings against predefined safety thresholds and classifies each subsystem as `NORMAL`, `WARNING`, or `CRITICAL`.

This helps distinguish unusual readings from conditions that may require immediate attention.

### 3. Alerts & Recommendations (`alerts.py`) — Turning Problems into Action

Identifying an issue is only part of the job. Operators also need to understand its importance.

The alert system:

- Converts detected problems into clear messages.
- Gives critical alerts higher priority than warnings.
- Provides recommendations based on the detected condition.

The aim is to make important information easier to understand at a glance.

### 4. Mission Control Dashboard (`main.py`) — One Place to See It All

The dashboard brings the different components together through an interactive Streamlit interface.

Operators can:

- View current spacecraft readings.
- Switch between simulated mission scenarios.
- Update telemetry step by step.
- Monitor overall mission status.
- View prioritized alerts and recommendations.
- Track changes in readings through historical trend charts.
- Reset the simulation when needed.

The dashboard uses Streamlit session state to maintain simulation progress between interactions.

## 🔄 The ASTRA Workflow

**Simulate → Validate → Detect → Alert → Monitor**

1. The simulator generates spacecraft telemetry.
2. The validator checks the incoming data.
3. The detector identifies and classifies unusual conditions.
4. The alert system prioritizes issues and suggests responses.
5. The dashboard presents the information in one place.

Each component has a specific responsibility, allowing the team to develop and connect the system in separate modules.

## 📂 Project Structure

```text
ASTRA/
│
├── simulator.py    # Generates simulated spacecraft readings
├── validator.py    # Checks incoming data for errors
├── detector.py     # Classifies subsystem conditions
├── alerts.py       # Creates prioritized alerts and recommendations
├── main.py         # Runs the interactive Streamlit dashboard
│
└── README.md       # Project overview and documentation
```

## 💡 Why ASTRA?

Spacecraft monitoring involves more than collecting numbers. Mission operators need reliable information, a clear picture of system conditions, and a way to recognize which issues deserve attention first.

ASTRA explores this challenge through a modular, interactive prototype that brings simulated telemetry and system monitoring together.

**Our goal is simple: turn spacecraft readings into information that is easier to understand, monitor, and act on.**

*ASTRA is a simulation-based prototype. It does not connect to real spacecraft or autonomously control spacecraft systems.*
