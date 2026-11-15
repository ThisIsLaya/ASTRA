
from validator import validate_telemetry


def detect_anomalies(data):
    """
    Detect spacecraft anomalies.

    Classifies readings as:
    NORMAL, WARNING or CRITICAL.
    """

    validation = validate_telemetry(data)

    anomalies = []

    # Invalid telemetry
    if not validation["is_valid"]:
        return {
            "overall_status": "CRITICAL",
            "anomalies": [
                {
                    "system": "DATA",
                    "severity": "CRITICAL",
                    "message": error
                }
                for error in validation["errors"]
            ],
            "validation": validation
        }

    # Battery detection
    battery = data["battery"]

    if battery < 30:
        anomalies.append({
            "system": "BATTERY",
            "severity": "CRITICAL",
            "message": f"Critical battery level: {battery}%"
        })

    elif battery <= 70:
        anomalies.append({
            "system": "BATTERY",
            "severity": "WARNING",
            "message": f"Low battery level: {battery}%"
        })

    # Oxygen detection
    oxygen = data["oxygen"]

    if oxygen < 50:
        anomalies.append({
            "system": "OXYGEN",
            "severity": "CRITICAL",
            "message": f"Critical oxygen level: {oxygen}%"
        })

    elif oxygen <= 70:
        anomalies.append({
            "system": "OXYGEN",
            "severity": "WARNING",
            "message": f"Low oxygen level: {oxygen}%"
        })

    # Temperature detection
    temperature = data["temperature"]

    if temperature < 10 or temperature > 40:
        anomalies.append({
            "system": "TEMPERATURE",
            "severity": "CRITICAL",
            "message": f"Dangerous cabin temperature: {temperature}°C"
        })

    elif temperature < 18 or temperature > 30:
        anomalies.append({
            "system": "TEMPERATURE",
            "severity": "WARNING",
            "message": f"Unusual cabin temperature: {temperature}°C"
        })

    # Communication detection
    if not data["communication"]:
        anomalies.append({
            "system": "COMMUNICATION",
            "severity": "CRITICAL",
            "message": "Communication with spacecraft has been lost."
        })

    # Outdated telemetry warning
    for warning in validation["warnings"]:
        anomalies.append({
            "system": "DATA",
            "severity": "WARNING",
            "message": warning
        })

    # Determine overall status
    if any(a["severity"] == "CRITICAL" for a in anomalies):
        overall_status = "CRITICAL"

    elif any(a["severity"] == "WARNING" for a in anomalies):
        overall_status = "WARNING"

    else:
        overall_status = "NORMAL"

    return {
        "overall_status": overall_status,
        "anomalies": anomalies,
        "validation": validation
    }
