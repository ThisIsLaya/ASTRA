import random
from datetime import datetime

# Initial spacecraft readings
INITIAL_STATE = {
    "battery": 90,
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
    Generate simulated spacecraft telemetry with natural up-and-down fluctuations.
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

    # Normal spacecraft operation: natural fluctuations (up and down)
    if scenario == "normal":
        # Battery can go down or up slightly (solar panel recharge)
        spacecraft["battery"] = max(
            20, min(100, spacecraft["battery"] + random.choice([-2, -1, 0, 1, 2]))
        )

        # Oxygen fluctuates slightly
        spacecraft["oxygen"] = max(
            60, min(100, spacecraft["oxygen"] + random.choice([-1, 0, 1]))
        )

        # Temperature fluctuates around safe range
        spacecraft["temperature"] = max(
            18, min(28, spacecraft["temperature"] + random.choice([-1, 0, 1]))
        )

        spacecraft["communication"] = True

    # Battery emergency: mostly drops, but can occasionally fluctuate slightly
    elif scenario == "battery_emergency":
        spacecraft["battery"] = max(
            0, min(100, spacecraft["battery"] + random.choice([-5, -3, 1]))
        )
        spacecraft["oxygen"] = max(50, min(100, spacecraft["oxygen"] + random.choice([-1, 0, 1])))
        spacecraft["temperature"] += random.choice([-1, 0, 1])

    # Oxygen anomaly: fluctuates around low/critical levels
    elif scenario == "oxygen_anomaly":
        spacecraft["oxygen"] = max(
            30, min(65, spacecraft["oxygen"] + random.choice([-2, -1, 1, 2]))
        )
        spacecraft["battery"] = max(0, min(100, spacecraft["battery"] + random.choice([-1, 0, 1])))

    # Temperature anomaly: fluctuates in high/dangerous ranges
    elif scenario == "temperature_anomaly":
        spacecraft["temperature"] = max(
            33, min(45, spacecraft["temperature"] + random.choice([-2, -1, 1, 2]))
        )
        spacecraft["battery"] = max(0, min(100, spacecraft["battery"] + random.choice([-1, 0, 1])))

    # Communication blackout
    elif scenario == "communication_blackout":
        spacecraft["communication"] = False
        # Readings can still drift during blackout
        spacecraft["battery"] = max(0, min(100, spacecraft["battery"] + random.choice([-1, 0, 1])))
        return spacecraft.copy()

    # Record the time of the latest successful reading
    spacecraft["timestamp"] = datetime.now().isoformat(
        timespec="seconds"
    )

    return spacecraft.copy()