
import importlib
from datetime import datetime

import streamlit as st


def _import_symbol(module_name, symbol_name):
    """Import a symbol from a sibling module in both script and package contexts."""
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        if __package__:
            module = importlib.import_module(f".{module_name}", __package__)
        else:
            raise

    return getattr(module, symbol_name)


generate_telemetry = _import_symbol("simulator", "generate_telemetry")
reset_simulator = _import_symbol("simulator", "reset_simulator")
validate_telemetry = _import_symbol("validator", "validate_telemetry")
detect_anomalies = _import_symbol("detector", "detect_anomalies")
generate_alerts = _import_symbol("alerts", "generate_alerts")


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ASTRA Mission Control",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================

def get_mission_status(results):
    """Determine the overall mission status from detection results."""

    if not isinstance(results, dict):
        return "UNKNOWN"

    status = results.get(
        "overall_status",
        results.get("status", "NORMAL")
    )

    return str(status).upper()


def get_alert_list(alert_results):
    """Convert alert results into a list for dashboard display."""

    if isinstance(alert_results, list):
        return alert_results

    if isinstance(alert_results, dict):
        if isinstance(alert_results.get("alerts"), list):
            return alert_results["alerts"]

        if "severity" in alert_results or "title" in alert_results:
            return [alert_results]

    return []


def get_alert_details(alert):
    """Extract display information from an alert."""

    if isinstance(alert, str):
        return {
            "severity": "WARNING",
            "title": alert,
            "message": alert,
            "recommendation": "Review the alert."
        }

    if not isinstance(alert, dict):
        return {
            "severity": "WARNING",
            "title": "Unrecognised alert",
            "message": str(alert),
            "recommendation": "Review the alert."
        }

    return {
        "severity": str(alert.get("severity", "WARNING")).upper(),
        "title": alert.get("title", alert.get("parameter", "Spacecraft alert")),
        "message": alert.get("message", alert.get("description", "An issue was detected.")),
        "recommendation": alert.get(
            "recommendation",
            alert.get("suggested_action", "Review spacecraft telemetry.")
        )
    }


def severity_icon(severity):
    """Choose an icon based on alert severity."""

    if severity == "CRITICAL":
        return "🔴"
    elif severity == "WARNING":
        return "🟠"
    else:
        return "🔵"


# ============================================================
# 3. SESSION STATE
# ============================================================

# Streamlit reruns the script whenever a user interacts
# with the dashboard.
#
# Session state allows us to preserve information between reruns.

if "telemetry" not in st.session_state:
    st.session_state.telemetry = None

if "history" not in st.session_state:
    st.session_state.history = []

if "acknowledged" not in st.session_state:
    st.session_state.acknowledged = set()

if "previous_scenario" not in st.session_state:
    st.session_state.previous_scenario = None


# ============================================================
# 4. DASHBOARD HEADER
# ============================================================

st.title("🚀 ASTRA Mission Control")

st.caption(
    "Autonomous Spacecraft Telemetry & Risk Assistant | "
    "Astra-1 Mars Transit Mission"
)

st.divider()


# ============================================================
# 5. SCENARIO SELECTION
# ============================================================

scenarios = {
    "Normal Operation": "normal",
    "Battery Emergency": "battery_emergency",
    "Oxygen Anomaly": "oxygen_anomaly",
    "Temperature Anomaly": "temperature_anomaly",
    "Communication Blackout": "communication_blackout"
}

selected_label = st.selectbox(
    "Select Mission Scenario",
    list(scenarios.keys())
)

selected_scenario = scenarios[selected_label]

# Detect whether the operator has changed the scenario.

scenario_changed = (
    st.session_state.previous_scenario != selected_scenario
)

if scenario_changed:
    st.session_state.history = []
    st.session_state.acknowledged = set()


# ============================================================
# 6. OPERATOR CONTROLS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    next_reading = st.button(
        "🔄 Generate Next Reading",
        use_container_width=True
    )

with col2:
    reset_button = st.button(
        "↩ Reset Simulation",
        use_container_width=True
    )

with col3:
    st.info("Simulation Mode")


# Generate an initial reading, a reading for a new scenario,
# or another reading when the operator presses the button.

if (
    st.session_state.telemetry is None
    or scenario_changed
    or next_reading
    or reset_button
):

    if reset_button:
        reset_simulator()

    data = generate_telemetry(selected_scenario)

    st.session_state.telemetry = data
    st.session_state.previous_scenario = selected_scenario

    # Keep a record of the readings for mission history.

    if data.get("timestamp") is not None:
        st.session_state.history.append(data.copy())

        # Keep the latest 50 readings to limit stored history.
        st.session_state.history = st.session_state.history[-50:]


# Current spacecraft telemetry.

data = st.session_state.telemetry


# ============================================================
# 7. VALIDATION AND ANOMALY DETECTION
# ============================================================

try:
    # Check whether the incoming telemetry is valid.

    validation_results = validate_telemetry(data)

    # Identify unusual spacecraft readings.

    detection_results = detect_anomalies(data)

    # Generate alerts using the detector's results.

    alert_results = generate_alerts(detection_results)

    # Convert alert output into a consistent list.

    alerts = get_alert_list(alert_results)

    mission_status = get_mission_status(detection_results)

except Exception as error:
    st.error(f"Unable to process telemetry: {error}")
    st.stop()


# ============================================================
# 8. MISSION STATUS
# ============================================================

st.subheader("Mission Overview")

if mission_status == "CRITICAL":
    st.error("🔴 CRITICAL: Immediate operator review required.")

elif mission_status == "WARNING":
    st.warning("🟠 WARNING: An unusual condition has been detected.")

elif mission_status == "NORMAL":
    st.success("🟢 NORMAL: No detected anomalies.")

else:
    st.info(f"Mission status: {mission_status}")


# ============================================================
# 9. SPACECRAFT TELEMETRY CARDS
# ============================================================

st.subheader("Spacecraft Telemetry")

battery_col, oxygen_col, temp_col, comm_col = st.columns(4)

with battery_col:
    st.metric(
        "🔋 Battery",
        f"{data['battery']}%"
    )

with oxygen_col:
    st.metric(
        "🫁 Oxygen",
        f"{data['oxygen']}%"
    )

with temp_col:
    st.metric(
        "🌡 Temperature",
        f"{data['temperature']} °C"
    )

with comm_col:
    if data["communication"]:
        st.metric("📡 Communication", "ONLINE")
    else:
        st.metric("📡 Communication", "OFFLINE")


# Display the timestamp of the latest received telemetry.

st.caption(
    f"Last successful telemetry timestamp: "
    f"{data.get('timestamp') or 'Unavailable'}"
)


# ============================================================
# 10. VALIDATION RESULTS
# ============================================================

st.divider()
st.subheader("Data Validation")

if isinstance(validation_results, dict):

    is_valid = validation_results.get(
        "valid",
        validation_results.get("is_valid", True)
    )

    if is_valid:
        st.success("Telemetry validation passed.")
    else:
        st.warning("Telemetry validation identified an issue.")

    errors = validation_results.get(
        "errors",
        validation_results.get("issues", [])
    )

    if errors:
        for error in errors:
            st.write(f"• {error}")

else:
    st.info("Validation completed.")


# ============================================================
# 11. ALERT PANEL
# ============================================================

st.divider()
st.subheader("🚨 Active Mission Alerts")

if not alerts:

    st.success("No alerts generated.")

else:

    for index, alert in enumerate(alerts):

        details = get_alert_details(alert)

        severity = details["severity"]

        # Create a consistent identifier for acknowledgement.

        alert_id = (
            f"{severity}:"
            f"{details['title']}:"
            f"{details['message']}"
        )

        acknowledged = (
            alert_id in st.session_state.acknowledged
        )

        with st.container(border=True):

            st.write(
                f"{severity_icon(severity)} "
                f"**{severity}: {details['title']}**"
            )

            st.write(details["message"])

            st.info(
                f"Suggested action: {details['recommendation']}"
            )

            if acknowledged:
                st.success("Alert acknowledged.")

            else:
                if st.button(
                    "Acknowledge Alert",
                    key=f"ack_{index}"
                ):
                    st.session_state.acknowledged.add(alert_id)
                    st.rerun()


# ============================================================
# 12. OPERATOR RESPONSE CHECKLIST
# ============================================================

st.divider()
st.subheader("☑ Operator Response Checklist")

st.write(
    "Use this checklist to organise the review of an alert. "
    "These are general demonstration steps, not spacecraft "
    "operating instructions."
)

checklist_items = [
    "Review the latest telemetry readings.",
    "Check the timestamp and communication status.",
    "Review the detected anomaly and its severity.",
    "Read the suggested response.",
    "Escalate the issue according to approved mission procedures."
]

for index, item in enumerate(checklist_items):

    st.checkbox(
        item,
        key=f"checklist_{index}"
    )


# ============================================================
# 13. TELEMETRY HISTORY
# ============================================================

st.divider()
st.subheader("📊 Mission Telemetry History")

if st.session_state.history:

    # Display the previous readings.

    st.line_chart(
        st.session_state.history,
        x="timestamp",
        y=["battery", "oxygen", "temperature"]
    )

    with st.expander("View Reading History"):

        st.dataframe(
            st.session_state.history,
            use_container_width=True
        )

else:
    st.info("No telemetry history available yet.")


# ============================================================
# 14. MISSION FOOTER
# ============================================================

st.divider()

st.caption(
    "ASTRA | Mission Control Decision-Support System | "
    "All spacecraft readings are simulated demonstration data."
)
