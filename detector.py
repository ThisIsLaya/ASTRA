from validator import validate_telemetry


def detect_anomalies(data):
    """
    Validate telemetry and classify each subsystem as NORMAL, WARNING, or CRITICAL.
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

    # Determine overall mission status
    statuses = [info["status"] for info in systems.values()]
    if "CRITICAL" in statuses:
        overall_status = "CRITICAL"
    elif "WARNING" in statuses:
        overall_status = "WARNING"
    else:
        overall_status = "NORMAL"

    return {
        "overall_status": overall_status,
        "is_valid": True,
        "validation_errors": [],
        "systems": systems,
        "timestamp": data["timestamp"]
    }


# Quick self-test for Person 2 checklist (missing, invalid, warning, critical)
if __name__ == "__main__":
    print("--- Test 1: Normal Data ---")
    print(detect_anomalies({"battery": 85, "oxygen": 95, "temperature": 22, "communication": True, "timestamp": "2026-11-15T12:00:00"}))

    print("\n--- Test 2: Warning & Critical Data ---")
    print(detect_anomalies({"battery": 35, "oxygen": 55, "temperature": 22, "communication": False, "timestamp": "2026-11-15T12:01:00"}))

    print("\n--- Test 3: Missing / Invalid Data ---")
    print(detect_anomalies({"battery": 150, "oxygen": None, "temperature": "hot"}))
