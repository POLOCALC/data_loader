# POLOCALC Data Loader

This repository provides tools to load and visualize data from drone missions, including drone logs, payload sensor data, Litchi flight logs, and (optionally) photogrammetry data.

## DataHandler Example

This example demonstrates how to load drone and payload sensor data using the `DataHandler` class and plot inclinometer pitch over time.

### Requirements

Ensure you have the following Python packages installed:

* `matplotlib`
* `pandas`
* Your local `datahandler` module and its dependencies (e.g., `DJIDrone`, `IMUSensor`, etc.)

### Example

```python
from datahandler import DataHandler
import matplotlib.pyplot as plt

# Define the base directory for the campaign and the flight number
dirpath = "/data/POLOCALC/campaigns/2025_04"
num = 522

# Initialize and load all available data
DH = DataHandler(num=num, dirpath=dirpath)
DH.load_data()

# Plot pitch from the inclinometer sensor
plt.figure()
plt.plot(DH.payload.inclino.data["datetime"], DH.payload.inclino.data["pitch"])
plt.xlabel("Time")
plt.ylabel("Pitch (degrees)")
plt.title("Inclinometer Pitch Over Time")
plt.grid(True)
plt.show()
```

---

## Utilities

This repository also contains two Python scripts designed for quick visualization and structured export of sensor log data:

* \`\` – Generates plots and a descriptive PDF summary report.
* \`\` – Processes raw sensor logs and converts them into clean, time-aligned CSV files.

### quick\_look.py – Quick Visualization

This script is used for exploratory analysis and test validation. It creates a multi-page PDF containing:

* Line plots (e.g., GPS position, accelerometer, barometer).
* Sampling time diagnostics.

### process\_data.py – CSV Export

Converts raw logs into aligned CSV files suitable for downstream analysis or archiving.

### ▶️ Example Usage

```bash
python utils/quick_look.py /path/to/logs
python utils/process_data.py /path/to/logs
```
