
def generate_alerts(results):
    alerts = []

    recommendations = {
        "BATTERY": "Check the battery and reduce power usage.",
        "OXYGEN": "Check the oxygen supply.",
        "TEMPERATURE": "Check the temperature control system.",
        "COMMUNICATION": "Check the communication system.",
        "DATA": "Check the sensor data."
    }

    for anomaly in results["anomalies"]:
        system = anomaly["system"]
        severity = anomaly["severity"]
        message = anomaly["message"]

        alert = {
            "system": system,
            "severity": severity,
            "message": message,
            "recommendation": recommendations.get(
                system, "Check the system."
            )
        }

        alerts.append(alert)

    # Put critical alerts first
    alerts.sort(
        key=lambda alert: 0 if alert["severity"] == "CRITICAL" else 1
    )

    return alerts


# Testing
if __name__ == "__main__":
    test_results = {
        "overall_status": "CRITICAL",
        "anomalies": [
            {
                "system": "BATTERY",
                "severity": "CRITICAL",
                "message": "Battery is too low"
            },
            {
                "system": "TEMPERATURE",
                "severity": "WARNING",
                "message": "Temperature is too high"
            }
        ]
    }

    print(generate_alerts(test_results))
