from validator import validate_telemetry


def detect_anomalies(data):
    """
    Validate telemetry, classify each subsystem, and extract anomalies 
    for the alerts module.
    """
    validation = validate_telemetry(data)

    # If telemetry data itself is invalid/corrupted, immediately flag CRITICAL
    if not validation["is_valid"]:
        return {
            "overall_status": "CRITICAL",
            "is_valid": False,
            "validation_errors": validation["errors"],
            "systems": {
                "validation": {
                    "status": "CRITICAL",
                    "value": None,
                    "message": "; ".join(validation["errors"])
                }
            },
            "anomalies": [
                {
                    "system": "Validation",
                    "severity": "CRITICAL",
                    "message": "; ".join(validation["errors"]),
                    "value": None
                }
            ],
            "timestamp": data.get("timestamp", "UNKNOWN") if isinstance(data, dict) else "UNKNOWN"
        }

    systems = {}

    # 1. Battery Detection
    battery = data["battery"]
    if battery <= 20:
        systems["battery"] = {"status": "CRITICAL", "value": battery, "message": f"Critical battery depletion ({battery}%)"}
    elif battery <= 40:
        systems["battery"] = {"status": "WARNING", "value": battery, "message": f"Low battery level ({battery}%)"}
    else:
        systems["battery"] = {"status": "NORMAL", "value": battery, "message": "Battery nominal"}

    # 2. Oxygen Detection
    oxygen = data["oxygen"]
    if oxygen <= 60:
        systems["oxygen"] = {"status": "CRITICAL", "value": oxygen, "message": f"Critical oxygen drop ({oxygen}%)"}
    elif oxygen <= 80:
        systems["oxygen"] = {"status": "WARNING", "value": oxygen, "message": f"Reduced oxygen level ({oxygen}%)"}
    else:
        systems["oxygen"] = {"status": "NORMAL", "value": oxygen, "message": "Oxygen nominal"}

    # 3. Cabin Temperature Detection
    temp = data["temperature"]
    if temp >= 35 or temp <= 5:
        systems["temperature"] = {"status": "CRITICAL", "value": temp, "message": f"Extreme cabin temperature ({temp} °C)"}
    elif temp >= 29 or temp <= 15:
        systems["temperature"] = {"status": "WARNING", "value": temp, "message": f"Abnormal cabin temperature ({temp} °C)"}
    else:
        systems["temperature"] = {"status": "NORMAL", "value": temp, "message": "Cabin temperature nominal"}

    # 4. Communication Link Detection
    comm = data["communication"]
    if not comm:
        systems["communication"] = {"status": "CRITICAL", "value": comm, "message": "Communication blackout — link lost"}
    else:
        systems["communication"] = {"status": "NORMAL", "value": comm, "message": "Communication link active"}

    # Determine overall mission status and collect anomalies
    statuses = [info["status"] for info in systems.values()]
    if "CRITICAL" in statuses:
        overall_status = "CRITICAL"
    elif "WARNING" in statuses:
        overall_status = "WARNING"
    else:
        overall_status = "NORMAL"

    # Build anomalies list for alerts.py
    anomalies = []
    for sys_name, info in systems.items():
        if info["status"] != "NORMAL":
            anomalies.append({
                "system": sys_name.capitalize(),
                "severity": info["status"],
                "message": info["message"],
                "value": info["value"]
            })

    return {
        "overall_status": overall_status,
        "is_valid": True,
        "validation_errors": [],
        "systems": systems,
        "anomalies": anomalies,  # Fixed: Added this key for alerts.py
        "timestamp": data["timestamp"]
    }
