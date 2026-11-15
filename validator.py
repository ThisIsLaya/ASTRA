
import random
from datetime import datetime

# Starting spacecraft readings
def reset_simulator():
    global spacecraft, active_scenario

    spacecraft = {
        "battery": 100,
        "oxygen": 95,
        "temperature": 22,
        "communication": True,
        "timestamp": datetime.now().isoformat()
    }

    active_scenario = None


reset_simulator()


def generate_telemetry(scenario="normal"):
    global active_scenario

    scenarios = [
        "normal",
        "battery_failure",
        "oxygen_problem",
        "temperature_problem",
        "communication_loss"
    ]

    if scenario not in scenarios:
        raise ValueError("Invalid scenario")

    # Start fresh when switching to another scenario,
    # except when communication is lost.
    if scenario != active_scenario:
        if scenario != "communication_loss":
            reset_simulator()

        active_scenario = scenario

    # Communication loss: keep the last readings
    if scenario == "communication_loss":
        spacecraft["communication"] = False
        return spacecraft.copy()

    spacecraft["communication"] = True

    if scenario == "normal":
        spacecraft["battery"] -= random.randint(0, 1)
        spacecraft["oxygen"] -= random.randint(0, 1)
        spacecraft["temperature"] += random.choice([-1, 1])

        spacecraft["temperature"] = max(
            18, min(26, spacecraft["temperature"])
        )

    elif scenario == "battery_failure":
        spacecraft["battery"] = max(
            0, spacecraft["battery"] - 10
        )

    elif scenario == "oxygen_problem":
        spacecraft["oxygen"] = max(
            0, spacecraft["oxygen"] - 8
        )

    elif scenario == "temperature_problem":
        spacecraft["temperature"] = 38

    spacecraft["timestamp"] = datetime.now().isoformat()

    return spacecraft.copy()
