
def generate_alerts(status):

    alerts = []

    recommendations = {
        "battery": "Check the spacecraft power system.",
        "oxygen": "Check the oxygen supply.",
        "temperature": "Check the temperature control system.",
        "communication": "Check the communication connection."
    }

    # Show critical problems first
    for level in ["CRITICAL", "WARNING"]:

        for system, condition in status.items():

            if condition == level:
                message = (
                    f"{level}: {system.capitalize()} problem. "
                    f"{recommendations[system]}"
                )

                alerts.append(message)

    return alerts
