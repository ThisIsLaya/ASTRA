
import random
from datetime import datetime


# Initial spacecraft readings
INITIAL_STATE = {
    "battery": 100,
    "oxygen": 95,
    "temperature": 22,
    "communication": True,
    "timestamp": None
}

# Current simulator state
spacecraft = INITIAL_STATE.copy()
active_scenario = None


def reset_simulator():
    """Reset the spacecraft to its initial state."""
    global spacecraft, active_scenario

    spacecraft = INITIAL_STATE.copy()
    active_scenario = None


def generate_telemetry(scenario="normal"):
    """
    Generate simulated spacecraft telemetry.

    Supported scenarios:
    normal
    battery_emergency
    oxygen_anomaly
    temperature_anomaly
    communication_blackout
    """

    global spacecraft, active_scenario

    valid_scenarios = [
        "normal",
        "battery_emergency",
        "oxygen_anomaly",
        "temperature_anomaly",
        "communication_blackout"
    ]

    if scenario not in valid_scenarios:
        raise ValueError(f"Unknown scenario: {scenario}")

    # Start a fresh simulation when the scenario changes
    if scenario != active_scenario:
        reset_simulator()
        active_scenario = scenario

    # Normal spacecraft operation
    if scenario == "normal":
        spacecraft["battery"] = max(
            0, spacecraft["battery"] - random.randint(0, 2)
        )

        spacecraft["oxygen"] = max(
            0, spacecraft["oxygen"] - random.randint(0, 1)
        )

        spacecraft["temperature"] += random.choice([-1, 0, 0, 1])

        spacecraft["communication"] = True

    # Battery emergency
    elif scenario == "battery_emergency":
        spacecraft["battery"] = max(
            0, spacecraft["battery"] - random.randint(8, 12)
        )

    # Oxygen anomaly
    elif scenario == "oxygen_anomaly":
        spacecraft["oxygen"] = 55

    # Temperature anomaly
    elif scenario == "temperature_anomaly":
        spacecraft["temperature"] = 38

    # Communication blackout
    elif scenario == "communication_blackout":
        spacecraft["communication"] = False

        # No new telemetry arrives during the blackout.
        # Keep the timestamp of the last successful reading.
        return spacecraft.copy()

    # Record the time of the latest successful reading
    spacecraft["timestamp"] = datetime.now().isoformat(
        timespec="seconds"
    )

    return spacecraft.copy()


if __name__ == "__main__":

    scenarios = [
        "normal",
        "battery_emergency",
        "oxygen_anomaly",
        "temperature_anomaly",
        "communication_blackout"
    ]

    for scenario in scenarios:
        reset_simulator()

        print(f"\n--- {scenario.upper()} ---")

        for reading in range(3):
            data = generate_telemetry(scenario)
            print(data)
