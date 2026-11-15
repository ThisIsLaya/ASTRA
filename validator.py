
from datetime import datetime, timezone


def validate_telemetry(data):

    errors = []

    # 1. Check for missing fields
    required_fields = [
        "timestamp",
        "battery",
        "oxygen",
        "temperature",
        "communication"
    ]

    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"Missing field: {field}")

    # Stop if required fields are missing
    if errors:
        return {
            "valid": False,
            "errors": errors
        }

    # 2. Check numeric data types
    numeric_fields = ["battery", "oxygen", "temperature"]

    for field in numeric_fields:
        value = data[field]

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{field} must be a number")

    # 3. Check value ranges
    if not errors:

        if not 0 <= data["battery"] <= 100:
            errors.append("Battery must be between 0 and 100")

        if not 0 <= data["oxygen"] <= 100:
            errors.append("Oxygen must be between 0 and 100")

        if not -100 <= data["temperature"] <= 100:
            errors.append("Temperature is outside the simulation range")

    # 4. Check communication status
    if data["communication"] not in ["ONLINE", "OFFLINE"]:
        errors.append("Invalid communication status")

    # 5. Check timestamp
    try:
        timestamp = datetime.fromisoformat(
            data["timestamp"].replace("Z", "+00:00")
        )

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        age = (
            datetime.now(timezone.utc) - timestamp
        ).total_seconds()

        if age > 120:
            errors.append("Telemetry data is outdated")

        if age < -10:
            errors.append("Timestamp is in the future")

    except (ValueError, TypeError, AttributeError):
        errors.append("Invalid timestamp format")

    # 6. Return result
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
