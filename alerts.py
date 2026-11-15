
from datetime import datetime


def generate_alerts(results):

    alerts = []

    recommendations = {
        "BATTERY": {
            "WARNING": "Monitor battery usage and reduce non-essential power consumption.",
            "CRITICAL": "Prioritize essential systems and investigate the power supply immediately."
        },
        "OXYGEN": {
            "WARNING": "Monitor oxygen levels and inspect the life-support system.",
            "CRITICAL": "Check the oxygen supply immediately and follow mission emergency procedures."
        },
        "TEMPERATURE": {
            "WARNING": "Monitor cabin temperature and check the thermal control system.",
            "CRITICAL": "Investigate the thermal control system and follow mission safety procedures."
        },
        "COMMUNICATION": {
            "WARNING": "Monitor signal stability and check communication equipment.",
            "CRITICAL": "Check communication equipment and attempt to restore contact with mission control."
        },
        "DATA": {
            "WARNING": "Check telemetry timestamps and request updated sensor readings.",
            "CRITICAL": "Verify sensor data integrity before making mission decisions."
        }
    }

    for anomaly in results.get("anomalies", []):
        system = anomaly["system"]
        severity = anomaly["severity"]
        message = anomaly["message"]

        recommendation = recommendations.get(system, {}).get(
            severity,
            "Review the affected system and investigate the anomaly."
        )

        alerts.append({
            "system": system,
            "severity": severity,
            "message": message,
            "recommendation": recommendation,
            "timestamp": datetime.now().isoformat(timespec="seconds")
        })

    priority = {
        "CRITICAL": 0,
        "WARNING": 1,
        "INFORMATIONAL": 2
    }

    alerts.sort(
        key=lambda alert: priority.get(alert["severity"], 3)
    )

    return alerts


if __name__ == "__main__":

    # Simulated output from detector.py
    test_results = {
        "overall_status": "CRITICAL",
        "anomalies": [
            {
                "system": "BATTERY",
                "severity": "CRITICAL",
                "message": "Critical battery level: 15%"
            },
            {
                "system": "TEMPERATURE",
                "severity": "WARNING",
                "message": "Unusual cabin temperature: 35°C"
            }
        ],
        "validation": {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
    }

    for alert in generate_alerts(test_results):
        print(alert)
