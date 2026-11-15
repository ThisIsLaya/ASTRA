"""Load historical ISS cabin telemetry exported from NASA OSDR EDA Data Tables."""
import csv
from pathlib import Path


def load_nasa_telemetry(path):
    """Return rows of actual NASA measurements, with their original timestamps.

    Do not invent battery, oxygen percentage, or communications readings.
    """
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        needed = {"Controller_Time_GMT", "Temp_degC_ISS"}
        if not needed.issubset(reader.fieldnames):
            raise ValueError(f"Expected NASA CSV columns: {sorted(needed)}. Found: {reader.fieldnames}")
        output = []
        for row in reader:
            try:
                temp = float(row["Temp_degC_ISS"])
                if not -100 <= temp <= 100:
                    continue
                item = {"historical_timestamp": row["Controller_Time_GMT"], "temperature": temp}
                for source, dest in [("CO2_ppm_ISS", "co2_ppm"), ("RH_percent_ISS", "humidity_percent")]:
                    try:
                        item[dest] = float(row[source])
                    except (KeyError, ValueError, TypeError):
                        pass
                output.append(item)
            except (ValueError, TypeError):
                continue
        if not output:
            raise ValueError("No valid ISS temperature measurements found")
        return output
