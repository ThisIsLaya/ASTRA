from validator import validate_telemetry


def detect_anomalies(data):
    """
    Validate telemetry, classify each subsystem, and extract anomalies
    formatted specifically for alerts.py and main.py.
    """
    validation = validate_telemetry(data)

    # If telemetry data itself is invalid/corrupted, immediately flag CRITICAL
    if not validation["is_valid"]:
        error_msg = "; ".join(validation["errors"])
        return {
            "overall_status": "CRITICAL",
            "is_valid": False,
            "validation_errors": validation["errors"],
            "systems": {
                "DATA": {
                    "status": "CRITICAL",
                    "value": None,
                    "message": error_msg
                }
            },
            "anomalies": [
                {
                    "system": "DATA",  # Matches recommendations["DATA"] in alerts.py
                    "severity": "CRITICAL",
                    "message": error_msg,
                    "value": None
                }
            ],
            "timestamp": data.get("timestamp", "UNKNOWN") if isinstance(data, dict) else "UNKNOWN"
        }

    systems = {}

    # 1. Battery Detection
    battery = data["battery"]
    if battery <= 20:
        systems["BATTERY"] = {"status": "CRITICAL", "value": battery, "message": f"Critical battery depletion ({battery}%)"}
    elif battery <= 40:
        systems["BATTERY"] = {"status": "WARNING", "value": battery, "message": f"Low battery level ({battery}%)"}
    else:
        systems["BATTERY"] = {"status": "NORMAL", "value": battery, "message": "Battery nominal"}

    # 2. Oxygen Detection
    oxygen = data["oxygen"]
    if oxygen <= 60:
        systems["OXYGEN"] = {"status": "CRITICAL", "value": oxygen, "message": f"Critical oxygen drop ({oxygen}%)"}
    elif oxygen <= 80:
        systems["OXYGEN"] = {"status": "WARNING", "value": oxygen, "message": f"Reduced oxygen level ({oxygen}%)"}
    else:
        systems["OXYGEN"] = {"status": "NORMAL", "value": oxygen, "message": "Oxygen nominal"}

    # 3. Cabin Temperature Detection
    temp = data["temperature"]
    if temp >= 35 or temp <= 5:
        systems["TEMPERATURE"] = {"status": "CRITICAL", "value": temp, "message": f"Extreme cabin temperature ({temp} °C)"}
    elif temp >= 29 or temp <= 15:
        systems["TEMPERATURE"] = {"status": "WARNING", "value": temp, "message": f"Abnormal cabin temperature ({temp} °C)"}
    else:
        systems["TEMPERATURE"] = {"status": "NORMAL", "value": temp, "message": "Cabin temperature nominal"}

    # 4. Communication Link Detection
    comm = data["communication"]
    if not comm:
        systems["COMMUNICATION"] = {"status": "CRITICAL", "value": comm, "message": "Communication blackout — link lost"}
    else:
        systems["COMMUNICATION"] = {"status": "NORMAL", "value": comm, "message": "Communication link active"}

    # Determine overall mission status
    statuses = [info["status"] for info in systems.values()]
    if "CRITICAL" in statuses:
        overall_status = "CRITICAL"
    elif "WARNING" in statuses:
        overall_status = "WARNING"
    else:
        overall_status = "NORMAL"

    # Build anomalies list with UPPERCASE system names for alerts.py
    anomalies = []
    for sys_name, info in systems.items():
        if info["status"] != "NORMAL":
            anomalies.append({
                "system": sys_name.upper(),
                "severity": info["status"],
                "message": info["message"],
                "value": info["value"]
            })

    return {
        "overall_status": overall_status,
        "is_valid": True,
        "validation_errors": [],
        "systems": systems,
        "anomalies": anomalies,
        "timestamp": data["timestamp"]
    }


# Standalone test for Person 2 checklist
if __name__ == "__main__":
    print("--- Test 1: Normal Data ---")
    print(detect_anomalies({"battery": 85, "oxygen": 95, "temperature": 22, "communication": True, "timestamp": "2026-11-15T12:00:00"}))

    print("\n--- Test 2: Warning & Critical Data ---")
    print(detect_anomalies({"battery": 35, "oxygen": 55, "temperature": 22, "communication": False, "timestamp": "2026-11-15T12:01:00"}))

    print("\n--- Test 3: Missing / Invalid Data ---")
    print(detect_anomalies({"battery": 150, "oxygen": None, "temperature": "hot"}))

