def validate_data(data):
    """Check if the telemetry data contains required keys and valid value ranges."""
    if not isinstance(data, dict):
        return False
    
    required_keys = ["battery", "oxygen", "temperature", "communication"]
    for key in required_keys:
        if key not in data:
            return False
    
    try:
        battery = float(data["battery"])
        oxygen = float(data["oxygen"])
        float(data["temperature"])
        
        if not (0 <= battery <= 100):
            return False
        if not (0 <= oxygen <= 100):
            return False
    except (ValueError, TypeError):
        return False

    return True


def validate_telemetry(reading):
    """Validate telemetry and return a dictionary with 'valid' status and error messages."""
    errors = []
    
    if not isinstance(reading, dict):
        return {"valid": False, "errors": ["Data must be a dictionary"]}
    
    required_keys = ["battery", "oxygen", "temperature", "communication"]
    for key in required_keys:
        if key not in reading:
            errors.append(f"Missing required key: {key}")

    if not errors:
        try:
            battery = float(reading["battery"])
            if not (0 <= battery <= 100):
                errors.append("Battery must be between 0 and 100")
        except (ValueError, TypeError):
            errors.append("Invalid battery value")

        try:
            oxygen = float(reading["oxygen"])
            if not (0 <= oxygen <= 100):
                errors.append("Oxygen must be between 0 and 100")
        except (ValueError, TypeError):
            errors.append("Invalid oxygen value")

        try:
            float(reading["temperature"])
        except (ValueError, TypeError):
            errors.append("Invalid temperature value")

        comm = reading.get("communication")
        if comm not in [True, False, "ONLINE", "OFFLINE"]:
            errors.append("Invalid communication status")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
