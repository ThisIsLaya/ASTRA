def validate_telemetry(data):
    """
    Validate incoming spacecraft telemetry dictionary.
    Returns a standardized dictionary: {"is_valid": bool, "errors": list[str]}
    """
    errors = []

    # 1. Check if data is a dictionary
    if not isinstance(data, dict):
        return {"is_valid": False, "errors": ["Telemetry payload must be a dictionary."]}

    # 2. Check required fields and data types
    required_fields = {
        "battery": (int, float),
        "oxygen": (int, float),
        "temperature": (int, float),
        "communication": bool,
        "timestamp": str
    }

    for field, expected_type in required_fields.items():
        if field not in data or data[field] is None:
            errors.append(f"Missing or null field: '{field}'")
        elif field == "communication" and not isinstance(data[field], bool):
            errors.append(f"Invalid type for '{field}': expected bool.")
        elif field != "communication" and isinstance(data[field], bool):
            errors.append(f"Invalid type for '{field}': cannot be bool.")
        elif not isinstance(data[field], expected_type):
            errors.append(f"Invalid type for '{field}': expected {expected_type}.")

    # Stop further range checks if basic fields/types are invalid
    if errors:
        return {"is_valid": False, "errors": errors}

    # 3. Check physical bounds (corrupted sensor values)
    if not (0 <= data["battery"] <= 100):
        errors.append(f"Battery out of physical bounds (0-100%): {data['battery']}")
    if not (0 <= data["oxygen"] <= 100):
        errors.append(f"Oxygen out of physical bounds (0-100%): {data['oxygen']}")
    if not (-100 <= data["temperature"] <= 150):
        errors.append(f"Temperature sensor reading corrupted: {data['temperature']} °C")
    if not data["timestamp"].strip():
        errors.append("Timestamp cannot be empty.")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }
