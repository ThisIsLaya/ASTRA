# Optional historical NASA replay; independent of simulated spacecraft readings.
from nasa_loader import load_nasa_telemetry
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="ASTRA Mission Control", page_icon="🚀", layout="wide")

source_mode = st.sidebar.radio("Telemetry source", ["Simulation", "NASA Historical Data"])
if source_mode == "NASA Historical Data":
    st.title("🚀 ASTRA — NASA Historical ISS Data")
    st.caption("Historical NASA OSDR ISS cabin measurements — not live telemetry")
    st.info("Battery, oxygen percentage and communication status are unavailable in this NASA dataset. They are deliberately not simulated in this mode.")
    csv_path = Path(__file__).parent / "data" / "nasa_iss.csv"
    if not csv_path.exists():
        st.warning("Download an ISS telemetry CSV from NASA EDA → Data Tables, and save it as data/nasa_iss.csv.")
        st.markdown("NASA source: https://visualization.osdr.nasa.gov/eda/")
        st.stop()
    try:
        records = load_nasa_telemetry(csv_path)
    except (ValueError, OSError) as exc:
        st.error(f"Could not load NASA CSV: {exc}")
        st.stop()
    index = st.slider("Historical reading", 0, len(records)-1, 0)
    reading = records[index]
    st.metric("ISS cabin temperature", f"{reading['temperature']:.1f} °C")
    if "co2_ppm" in reading:
        st.metric("ISS CO₂", f"{reading['co2_ppm']:.0f} ppm")
    if "humidity_percent" in reading:
        st.metric("ISS relative humidity", f"{reading['humidity_percent']:.1f}%")
    st.caption(f"Original NASA timestamp: {reading['historical_timestamp']}")
    st.line_chart(pd.DataFrame(records[:index+1]).set_index("historical_timestamp")[["temperature"]])
    st.warning("NASA historical readings are displayed without applying ASTRA's simulated oxygen/battery thresholds. These are not validated flight safety limits.")
    st.stop()

import streamlit as st
from simulator import generate_telemetry, reset_simulator
from detector import detect_anomalies
from alerts import generate_alerts

# Custom CSS styling for a cleaner look
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00d2ff;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #8a9ba8;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Dashboard header
st.markdown('<p class="main-title">🚀 ASTRA Mission Control</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Autonomous Spacecraft Telemetry & Risk Assistant</p>', unsafe_allow_html=True)

# Initialize session state
if "telemetry" not in st.session_state:
    st.session_state.telemetry = generate_telemetry("normal")
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar controls
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=300&auto=format&fit=crop", caption="ASTRA Orbital Unit")
    st.header("🎛️ Mission Controls")
    
    scenario = st.selectbox(
        "Select Simulation Scenario",
        [
            "normal",
            "battery_emergency",
            "oxygen_anomaly",
            "temperature_anomaly",
            "communication_blackout"
        ]
    )
    
    st.markdown("---")
    
    # Action buttons
    if st.button("🔄 Update Telemetry Reading", type="primary", use_container_width=True):
        new_data = generate_telemetry(scenario)
        st.session_state.telemetry = new_data
        st.session_state.history.append(new_data)

    if st.button("↺ Reset Spacecraft State", use_container_width=True):
        reset_simulator()
        st.session_state.telemetry = generate_telemetry("normal")
        st.session_state.history = []
        st.success("Spacecraft reset successfully!")

# Process current telemetry data
data = st.session_state.telemetry
detection_results = detect_anomalies(data)
alerts = generate_alerts(detection_results)

# Section 1: Overall Mission Status Banner
overall_status = detection_results["overall_status"]

if overall_status == "CRITICAL":
    st.error("🚨 CRITICAL STATUS: Immediate flight intervention required!")
elif overall_status == "WARNING":
    st.warning("⚠️ WARNING STATUS: Abnormal spacecraft conditions detected.")
else:
    st.success("✅ NOMINAL STATUS: All spacecraft systems operating normally.")

st.markdown("---")

# Section 2: Live Telemetry Metrics Grid
st.subheader("📊 Live Telemetry Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="🔋 Battery Level", value=f"{data['battery']}%", delta=f"{data['battery'] - 90}% relative")
with col2:
    st.metric(label="🫁 Oxygen Levels", value=f"{data['oxygen']}%")
with col3:
    st.metric(label="🌡️ Cabin Temperature", value=f"{data['temperature']} °C")
with col4:
    comm_status_text = "ONLINE" if data["communication"] else "OFFLINE"
    st.metric(label="📶 Comm Link", value=comm_status_text)

st.caption(f"🕒 Timestamp: {data['timestamp']} | 🎯 Active Scenario Mode: {scenario}")

st.markdown("---")

# Section 3: Active Alerts & Recommended Actions
st.subheader("🚨 Active Alerts & Recommended Actions")

if alerts:
    for alert in alerts:
        with st.container(border=True):
            sev = alert.get("severity", "WARNING")
            sys_name = alert.get("system", "System")
            msg = alert.get("message", "Unknown anomaly detected")
            rec = alert.get("recommendation", "Check subsystem status.")
            
            if sev == "CRITICAL":
                st.markdown(f"### 🔴 [CRITICAL] {sys_name}")
            else:
                st.markdown(f"### 🟡 [WARNING] {sys_name}")
                
            st.write(f"**Issue:** {msg}")
            st.info(f"💡 **Recommended Action:** {rec}")
            
            # Safe timestamp retrieval to prevent KeyError
            alert_time = alert.get("timestamp", data.get("timestamp", "N/A"))
            st.caption(f"Logged at: {alert_time}")
else:
    st.info("✨ No active alerts. All telemetry streams are stable and healthy.")

# Section 4: Telemetry Trend History Chart
if len(st.session_state.history) > 1:
    st.markdown("---")
    st.subheader("📈 Telemetry Trend Analysis")
    chart_data = {
        "Battery (%)": [item["battery"] for item in st.session_state.history],
        "Oxygen (%)": [item["oxygen"] for item in st.session_state.history],
        "Temperature (°C)": [item["temperature"] for item in st.session_state.history]
    }
    st.line_chart(chart_data)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8a9ba8;'>ASTRA Mission Control Center — Built with Python & Streamlit 🚀</p>", unsafe_allow_html=True)
