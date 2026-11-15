
def detect_problems(data):

    status = {}

    # Battery
    if data["battery"] < 30:
        status["battery"] = "CRITICAL"
    elif data["battery"] < 60:
        status["battery"] = "WARNING"
    else:
        status["battery"] = "NORMAL"

    # Oxygen
    if data["oxygen"] < 30:
        status["oxygen"] = "CRITICAL"
    elif data["oxygen"] < 60:
        status["oxygen"] = "WARNING"
    else:
        status["oxygen"] = "NORMAL"

    # Temperature
    if data["temperature"] > 35 or data["temperature"] < 5:
        status["temperature"] = "CRITICAL"
    elif data["temperature"] > 30 or data["temperature"] < 10:
        status["temperature"] = "WARNING"
    else:
        status["temperature"] = "NORMAL"

    # Communication
    if data["communication"] == False:
        status["communication"] = "CRITICAL"
    else:
        status["communication"] = "NORMAL"

    return status
