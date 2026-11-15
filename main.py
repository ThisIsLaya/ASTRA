
import streamlit as st
from datetime import datetime
import random

st.set_page_config(
    page_title="ASTRA Mission Control",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 ASTRA — Spacecraft Mission Control")
st.caption("Real-Time Telemetry Monitoring & Risk Assessment")

# Scenario selector
scenario = st.sidebar.selectbox(
    "Select Mission Scenario",
    ["Normal", "Low Battery", "Low Oxygen",
     "Overheating", "Communication Loss"]
)

# Temporary telemetry until simulator.py is connected
data = {
    "timestamp": datetime.now().isoformat(),
    "battery": random.randint(70, 100),
    "oxygen": random.randint(90, 100),
    "temperature": round(random.uniform(20, 25), 1),
    "communication": True
}

if scenario == "Low Battery":
    data["battery"] = 15
elif scenario == "Low Oxygen":
    data["oxygen"] = 65
elif scenario == "Overheating":
    data["temperature"] = 45
elif scenario == "Communication Loss":
    data["communication"] = False

# Dashboard metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("🔋 Battery", f"{data['battery']}%")
col2.metric("🫁 Oxygen", f"{data['oxygen']}%")
col3.metric("🌡️ Temperature", f"{data['temperature']}°C")
col4.metric(
    "📡 Communication",
    "Connected" if data["communication"] else "Disconnected"
)

# Temporary anomaly detection and recommendations
alerts = []

if data["battery"] < 20:
    alerts.append(("CRITICAL", "Battery level dangerously low",
                   "Switch to power-saving mode."))

if data["oxygen"] < 75:
    alerts.append(("CRITICAL", "Oxygen level dangerously low",
                   "Check oxygen supply and activate backup systems."))

if data["temperature"] > 35:
    alerts.append(("WARNING", "Cabin temperature too high",
                   "Inspect thermal control systems."))

if not data["communication"]:
    alerts.append(("CRITICAL", "Communication link lost",
                   "Attempt reconnection and check antenna systems."))

st.divider()

st.subheader("⚠️ Mission Status")

if any(a[0] == "CRITICAL" for a in alerts):
    st.error("🔴 CRITICAL — Immediate attention required")
elif alerts:
    st.warning("🟡 WARNING — Abnormal conditions detected")
else:
    st.success("🟢 NORMAL — All spacecraft systems operating normally")

st.subheader("🚨 Alerts & Recommended Actions")

if alerts:
    for severity, message, recommendation in alerts:
        with st.container(border=True):
            st.write(f"**{severity}: {message}**")
            st.write(f"Recommended Action: {recommendation}")
else:
    st.info("No active alerts.")

st.divider()
st.caption("ASTRA | Autonomous Spacecraft Telemetry & Risk Assistant")
