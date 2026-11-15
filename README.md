# 🚀 ASTRA — Spacecraft Telemetry & Emergency Monitoring System

**ASTRA** (Autonomous Spacecraft Telemetry & Risk Assistant) is an interactive mission control dashboard built with **Python** and **Streamlit**. It simulates real-time spacecraft telemetry, validates incoming sensor data, detects system anomalies, and generates prioritized alerts with actionable recommendations for flight operators.

---

## 🏗️ Project Architecture & Team Roles

The project is divided into four modular components connected via standardized Python dictionary contracts:

### 1️⃣ Telemetry Simulator (`simulator.py`) 
* Generates dynamic spacecraft sensor readings (`battery`, `oxygen`, `temperature`, `communication`, `timestamp`).
* Simulates natural fluctuations as well as critical mission scenarios (`normal`, `battery_emergency`, `oxygen_anomaly`, `temperature_anomaly`, `communication_blackout`).

### 2️⃣ Data Validation & Anomaly Detection (`validator.py`, `detector.py`) 
* **`validator.py`**: Verifies data integrity by checking required fields, strict data types, missing/null values, and physical sensor bounds.
* **`detector.py`**: Evaluates validated telemetry against safety thresholds and classifies each subsystem (`battery`, `oxygen`, `temperature`, `communication`) as **`NORMAL`**, **`WARNING`**, or **`CRITICAL`**.

### 3️⃣ Alerts & Recommendations (`alerts.py`) 
* Translates detected anomalies into structured, human-readable alerts.
* Prioritizes **`CRITICAL`** alerts above **`WARNING`** alerts and attaches targeted corrective recommendations.

### 4️⃣ Mission Control Dashboard (`main.py`) 
* Provides an interactive Streamlit web interface displaying live metrics, overall mission status banners, and prioritized alerts.
* Uses `st.session_state` to support step-by-step telemetry updates, scenario switching, spacecraft resets, and real-time trend history charts.

---

## 📂 File Structure

```text
ASTRA/
├── simulator.py    # Spacecraft telemetry simulation & emergency scenarios
├── validator.py    # Schema, type, and physical bounds validation
├── detector.py     # Threshold-based anomaly classification (NORMAL/WARNING/CRITICAL)
├── alerts.py       # Alert prioritization & recommended corrective actions
├── main.py         # Streamlit interactive mission control dashboard
└── README.md       # Project documentation
