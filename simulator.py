
import random
from datetime import datetime


# Starting spacecraft readings
INITIAL_STATE = {
    "battery": 100,
    "oxygen": 95,
    "temperature": 22,
    "communication": True,
    "timestamp": None
}

# Current spacecraft condition
spacecraft = INITIAL_STATE.copy()

# Keeps track of the selected scenario
active_scenario = None


def reset_simulator():
    """Reset all spacecraft readings to their starting values."""

    global spacecraft, active_scenario

    spacecraft = INITIAL_STATE.copy()
    active_scenario = None


def generate_telemetry(scenario="normal"):
    """
    Generate spacecraft telemetry based on the selected scenario.

    Available scenarios:
    normal
    battery_failure
    oxygen_problem
    temperature_problem
    communication_loss
    """

    global spacecraft, active_scenario

    valid_scenarios = [
        "normal",
        "battery_failure",
        "oxygen_problem",
        "temperature_problem",
        "communication_loss"
    ]

    # Check whether the scenario name is valid
    if scenario not in valid_scenarios:
        raise ValueError("Invalid scenario selected.")

    # Start a fresh simulation when switching scenarios,
    # except for communication loss, which preserves
    # the last successfully received readings.
    if scenario != active_scenario:

        if scenario != "communication_loss":
            reset_simulator()

        active_scenario = scenario

    # Normal spacecraft operation
    if scenario == "normal":

        spacecraft["battery"] = max(
            0, spacecraft["battery"] - random.randint(0, 1)
        )

        spacecraft["oxygen"] = max(
            0, spacecraft["oxygen"] - random.randint(0, 1)
        )

        # Temperature changes slightly with each update
        spacecraft["temperature"] += random.choice([-1, 1])

        # Communication is available
        spacecraft["communication"] = True

    # Battery emergency
    elif scenario == "battery_failure":

        spacecraft["battery"] = max(
            0, spacecraft["battery"] - random.randint(8, 12)
        )

    # Oxygen problem
    elif scenario == "oxygen_problem":

        spacecraft["oxygen"] = max(
            0, spacecraft["oxygen"] - random.randint(5, 10)
        )

    # Temperature problem
    elif scenario == "temperature_problem":

        spacecraft["temperature"] = 38

    # Communication loss
    elif scenario == "communication_loss":

        spacecraft["communication"] = False

        # If this is the first reading, record the last
        # known timestamp before the communication loss.
        if spacecraft["timestamp"] is None:
            spacecraft["timestamp"] = datetime.now().isoformat()

        # No new telemetry arrives, so return the old readings.
        return spacecraft.copy()

    # Update timestamp after every successful reading
    spacecraft["timestamp"] = datetime.now().isoformat()

    # Return a copy so other files cannot accidentally
    # modify the simulator's internal spacecraft state.
    return spacecraft.copy()


# Test the simulator independently
if __name__ == "__main__":

    scenarios = [
        "normal",
        "battery_failure",
        "oxygen_problem",
        "temperature_problem",
        "communication_loss"
    ]

    for scenario in scenarios:

        reset_simulator()

        print("\nSCENARIO:", scenario.upper())

        for i in range(3):

            data = generate_telemetry(scenario)

            print("Reading", i + 1, ":", data)
