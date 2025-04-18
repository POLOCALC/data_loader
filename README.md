# Data Loader

This repository provides the get_payload_data that contains function to read any sensors, and two Python scripts designed to assist in the quick visualization and structured export of sensor log data:

- [`quick_look.py`](#quick_lookpy-—-quick-visualization-and-report-generation): Generates plots and a descriptive PDF summary report.
- [`process_data.py`](#process_datapy-—-structured-csv-export-of-raw-sensor-data): Processes raw sensor logs and converts them into clean, time-aligned CSV files.

---

## `quick_look.py` — Quick Visualization and Report Generation

This script is designed for exploratory data analysis and test validation. It reads various raw sensor log files (in CSV format) and generates a multi-page PDF report that includes:

- Line plots for each type of data (e.g. GPS position, accelerometer values, barometric pressure, etc.).
- Sampling time diagnostics to evaluate timing consistency.

### ▶️ Usage

```bash
python quick_look.py path/to/logs
python process_data.py path/to/logs