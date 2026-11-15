# NASA Historical Data mode

1. Visit https://visualization.osdr.nasa.gov/eda/
2. Open **Data Tables**, select a mission, and export the **Telemetry Table** as CSV (not Summary).
3. Save the CSV at `data/nasa_iss.csv` (do not rename the columns).
4. Run `pip install -r requirements.txt` and `python -m streamlit run main.py`.
5. Select **NASA Historical Data** in the sidebar. Use the slider to replay recorded rows.

Required CSV columns: `Controller_Time_GMT`, `Temp_degC_ISS`. Optional: `CO2_ppm_ISS`, `RH_percent_ISS`.

This mode only displays NASA measurements. It does not claim battery, oxygen percentage, or communications status; those are not present in this CSV. The existing anomaly detector is designed for synthetic values and is **not** used for NASA measurements. Do not apply simulated thresholds to actual NASA telemetry without verifying units and appropriate operational limits.


RR-1 historical telemetry is already included in data/nasa_iss.csv, converted from the supplied NASA EDA telemetry table. Select NASA Historical Data in the sidebar. Historical data is displayed separately from synthetic simulation; no flight-safety thresholds are applied.
