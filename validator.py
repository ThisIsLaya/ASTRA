
from datetime import datetime

# Expected ranges
VALID_RANGES = {
    "battery": (0, 100),
    "oxygen": (0, 100),
    "temperature": (-50, 100)
}

MAX_DATA_AGE_SECONDS = 30


def validate_telemetry(data):
    """
    Validate spacecraft telemetry.

    Checks:
    - Missing values
    - Invalid data types
    - Values outside acceptable ranges
    - Invalid or outdated timestamps
    - Communication status
    """

    errors = []
    warnings = []

    required_fields = [
        "battery",
        "oxygen",
        "temperature",
        "communication",
        "timestamp"
    ]

    # Check if data is a dictionary
    if not isinstance(data, dict):
        return {
            "is_valid": False,
            "errors": ["Telemetry data must be a dictionary."],
            "warnings": []
        }

    # Check missing fields
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"Missing or empty field: {field}")

    # Stop if required data is missing
    if errors:
        return {
            "is_valid": False,
            "errors": errors,
            "warnings": warnings
        }

    # Validate numerical readings
    for field, (minimum, maximum) in VALID_RANGES.items():

        value = data[field]

        # Boolean values should not count as numbers
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{field} must be a number.")
            continue

        if not minimum <= value <= maximum:
            errors.append(
                f"{field} is outside the valid range ({minimum}-{maximum})."
            )

    # Validate communication
    if not isinstance(data["communication"], bool):
        errors.append("Communication must be True or False.")

    # Validate timestamp
    try:
        timestamp = datetime.fromisoformat(data["timestamp"])

        age = (datetime.now() - timestamp).total_seconds()

        if age < -5:
            errors.append("Timestamp is in the future.")

        elif age > MAX_DATA_AGE_SECONDS:
            warnings.append("Telemetry data is outdated.")

    except (ValueError, TypeError):
        errors.append("Invalid timestamp format.")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
