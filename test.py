
from datetime import datetime

from validator import validate_telemetry

data = {
    "timestamp": datetime.now().isoformat(),
    "battery": 78,
    "oxygen": 92,
    "temperature": 24.5,
    "communication": "ONLINE"
}

result = validate_telemetry(data)

print("VALIDATION RESULT:")
print(result)
