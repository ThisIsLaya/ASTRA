
import streamlit as st

from simulator import generate_telemetry, reset_simulator
from validator import validate_data
from detector import detect_problems
from alerts import generate_alerts


st.title("🚀 ASTRA")
st.subheader("Spacecraft Monitoring Dashboard")

# Choose a scenario
scenario = st.selectbox(
    "Choose a spacecraft scenario",
    [
        "normal",
        "battery_failure",
        "oxygen_problem",
        "temperature_problem",
        "communication_loss"
    ]
)

# Starting readings
if "telemetry" not in st.session_state:
    st.session_state.telemetry = generate_telemetry("normal")

# Update button
if st.button("Update Readings"):
    st.session_state.telemetry = generate_telemetry(scenario)

# Reset button
if st.button("Reset Spacecraft"):
    reset_simulator()
    st.session_state.telemetry = generate_telemetry("normal")

data = st.session_state.telemetry

st.divider()

# Display readings
st.subheader("Spacecraft Readings")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Battery", f"{data['battery']}%")
col2.metric("Oxygen", f"{data['oxygen']}%")
col3.metric("Temperature", f"{data['temperature']} °C")

connection = "ONLINE" if data["communication"] else "LOST"
col4.metric("Communication", connection)

st.caption("Last update: " + data["timestamp"])

st.divider()

# Check the data
st.subheader("System Status")

if validate_data(data):

    status = detect_problems(data)

    for system, condition in status.items():
        st.write(f"**{system.capitalize()}:** {condition}")

    # Generate alerts
    alerts = generate_alerts(status)

    st.divider()
    st.subheader("Alerts & Recommendations")

    if alerts:
        for alert in alerts:
            if alert.startswith("CRITICAL"):
                st.error(alert)
            else:
                st.warning(alert)
    else:
        st.success("All spacecraft systems are operating normally.")

else:
    st.error("Invalid spacecraft data!")
