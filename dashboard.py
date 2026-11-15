import streamlit as st

from simulator import generate_telemetry, reset_simulator
from validator import validate_telemetry
import detector
from alerts import generate_alerts


# The simulator uses True/False for communication, but the validator
# expects ONLINE/OFFLINE. The detector also expects different result keys.
def check_telemetry(data):
    reading = data.copy()
    reading["communication"] = "ONLINE" if data["communication"] else "OFFLINE"
    result = validate_telemetry(reading)
    return {
        "is_valid": result["valid"],
        "errors": result["errors"],
        "warnings": [],
    }


# Let the detector use the compatible validator without editing teammates' files.
detector.validate_telemetry = check_telemetry

st.set_page_config(page_title="ASTRA Mission Control", page_icon="🚀", layout="wide")
st.title("🚀 ASTRA Mission Control")
st.caption("Spacecraft telemetry and risk monitoring — simulated data")

scenarios = {
    "Normal Operation": "normal",
    "Battery Emergency": "battery_emergency",
    "Oxygen Anomaly": "oxygen_anomaly",
    "Temperature Anomaly": "temperature_anomaly",
    "Communication Blackout": "communication_blackout",
}

choice = st.selectbox("Choose a scenario", list(scenarios))
scenario = scenarios[choice]

if "data" not in st.session_state:
    st.session_state.data = None
    st.session_state.scenario = None
    st.session_state.history = []

left, right = st.columns(2)
with left:
    update = st.button("🔄 Update Telemetry Readings", use_container_width=True)
with right:
    reset = st.button("↩ Reset Simulation", use_container_width=True)

changed = st.session_state.scenario != scenario
if changed or reset:
    reset_simulator()
    st.session_state.history = []

if st.session_state.data is None or update or changed or reset:
    st.session_state.data = generate_telemetry(scenario)
    st.session_state.scenario = scenario
    if st.session_state.data["timestamp"] is not None:
        st.session_state.history.append(st.session_state.data.copy())

data = st.session_state.data
results = detector.detect_anomalies(data)

# When a blackout begins, the simulator has no successful timestamp.
# Still report the lost communication, even if validation fails first.
if not data["communication"]:
    if not any(a["system"] == "COMMUNICATION" for a in results["anomalies"]):
        results["anomalies"].append({
            "system": "COMMUNICATION",
            "severity": "CRITICAL",
            "message": "Communication with spacecraft has been lost.",
        })
    results["overall_status"] = "CRITICAL"

alerts = generate_alerts(results)
status = results["overall_status"]

st.subheader("Mission Status")
if status == "CRITICAL":
    st.error("🔴 CRITICAL — Immediate attention required")
elif status == "WARNING":
    st.warning("🟠 WARNING — Check spacecraft systems")
else:
    st.success("🟢 NORMAL — All monitored systems are okay")

st.subheader("Spacecraft Telemetry")
battery, oxygen, temperature, communication = st.columns(4)
battery.metric("🔋 Battery", f"{data['battery']}%")
oxygen.metric("🫁 Oxygen", f"{data['oxygen']}%")
temperature.metric("🌡️ Temperature", f"{data['temperature']}°C")
communication.metric("📡 Communication", "ONLINE" if data["communication"] else "OFFLINE")
st.caption(f"Last telemetry timestamp: {data['timestamp'] or 'No successful reading'}")

st.subheader("Alerts and Recommendations")
if not alerts:
    st.success("No active alerts")
else:
    for alert in alerts:
        st.write(f"**{alert['severity']} — {alert['system']}**")
        st.write(alert["message"])
        st.info(f"Recommended action: {alert['recommendation']}")

if len(st.session_state.history) > 1:
    st.subheader("Telemetry History")
    st.line_chart(st.session_state.history, x="timestamp", y=["battery", "oxygen", "temperature"])
