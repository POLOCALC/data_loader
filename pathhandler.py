import os
import numpy as np
import pandas as pd
import datetime
from pathlib import Path

from tools import read_log_time, get_path_from_keyword
from DJIDrone import DJIDrone

DATADIR = "/data/POLOCALC/campaigns"

def flightpath_from_num(num, dirpath=DATADIR):
    """
    Find the path to a flight log file with a given number.

    Parameters
    ----------
    num : int
        The number of the flight log to find.
    dir_path : str
        The root directory to search in. Defaults to
        ``/data/POLOCALC/campaigns/``.

    Returns
    -------
    str or None
        The path to the file if found, or ``None`` if the file is not found.
    """
    for root, _, _ in os.walk(dirpath):
        if os.path.isfile(os.path.join(root, f"FLY{num}.csv")):
            return os.path.join(root, f"FLY{num}.csv")
        
    print(f"[flightpath_from_num] No file found in {dirpath} for {num}.")
    return None 


def match_log_filename(drone, sensors_root_dir=DATADIR, time_delta=pd.Timedelta(minutes=10)):

    """
    Matches and retrieves the most relevant sensor log directory and its corresponding log file
    based on the timestamp of the drone data.

    Parameters
    ----------
    drone : DJIDrone or BlackSquareDrone (not implemented yet)
        An instance of a drone object that has already loaded data with a "GPS:dateTimeStamp" column.
    sensors_root_dir : str, optional
        Root directory where the sensor log directories are located. Default is `DATADIR`.
    time_delta : pd.Timedelta, optional
        Maximum allowable difference between drone and sensor timestamps for a valid match.
        Default is 10 minutes.

    Returns
    -------
    matched_sensors_dir : str or None
        Path to the matching 'sensors_data' directory. None if no suitable match is found.
    matched_logfile : str or None
        Path to the corresponding 'file.log'. None if no suitable match is found.

    Notes
    -----
    - Assumes the sensor logs have a standard layout: each subdirectory contains a `file.log`
      and a `sensors_data/` subdirectory.
    - Uses a hardcoded keyphrase to extract timestamps from log files.
    - Returns the closest match only if the time difference is within the threshold.
    """

    drone_tst = pd.to_datetime(drone.data["GPS:dateTimeStamp"], utc=True).iloc[0]

    matched_timestamps = []
    matched_dirs = []
    matched_logs = []

    for root, _, files in os.walk(sensors_root_dir):
        if "file.log" in files:
            logfile = os.path.join(root, "file.log")
            sensors_dir = os.path.join(root, "sensors_data")
            if not os.path.isdir(sensors_dir):
                continue
            # sensor_files = [f for f in os.listdir(sensors_dir) if f.startswith(SENSORS_DIR[sensor]["filename_prefix"])]
            # if not sensor_files:
            #     continue

            tst = read_log_time(keyphrase="INFO:Loaded configuration config/rover_config.yml", logfile=logfile)
            if tst is None:
                continue

            matched_timestamps.append(pd.to_datetime(tst, utc=True))
            matched_dirs.append(sensors_dir)
            matched_logs.append(logfile)

    if not matched_timestamps:
        print(f"[match_log_filename] No matches found for '{drone.path}'.")
        return None, None

    deltas = [abs(t - drone_tst) for t in matched_timestamps]
    min_delta = min(deltas)

    if min_delta <= time_delta:
        idx = deltas.index(min_delta)
        return matched_dirs[idx], matched_logs[idx]
    else:
        print(f"[match_log_filename] Found no files with time delta <({time_delta}) for '{drone.path}'.")
        return None, None
    
def match_litchi_filename(drone, litchi_dir=DATADIR, time_delta=pd.Timedelta(minutes=10)):    
    """
    Matches and retrieves the Litchi flight log file closest in time to the drone's
    recorded GPS timestamp.

    Parameters
    ----------
    drone : DJIDrone
        An instance of a drone object with a loaded "GPS:dateTimeStamp" column.
    litchi_dir : str, optional
        Directory where Litchi log files are stored. Defaults to `DATADIR`.
    time_delta : pd.Timedelta, optional
        Maximum allowable difference between the drone's and Litchi log's timestamps
        to consider it a valid match. Defaults to 10 minutes.

    Returns
    -------
    str or None
        Full path to the best-matching Litchi log file, or None if no suitable match is found.

    Notes
    -----
    - Filenames must follow the pattern "YYYY-MM-DD_HH-MM-SS_v2.csv".
    - The timestamp in filenames is assumed to be in local time (America/Santiago), and is
      converted to UTC before matching.
    - If no filenames can be parsed or if none match within the time threshold,
      the function returns None.
    """

    drone_tst = pd.to_datetime(drone.data["GPS:dateTimeStamp"], utc=True).iloc[0]

    #Look for litchi files with matching datetime
    litchi_files = get_path_from_keyword(litchi_dir, "_v2.csv") #[f for f in os.listdir(litchi_dir) if f.endswith("_v2.csv") and f.startswith("20")]
    if not litchi_files:
        print(f"[match_litchi_filename] No Litchi files found in {litchi_dir}")
        return None

    #Look for the closest litchi datetime to the drone data
    timestamps = []
    for f in litchi_files:
        try:
            ts = datetime.datetime.strptime(os.path.basename(f), "%Y-%m-%d_%H-%M-%S_v2.csv")
            timestamps.append(ts)
        except ValueError:
            print(f"[match_litchi_filename] Skipping unparseable filename: {f}")
            continue

    if not timestamps:
        print("[match_litchi_filename] No valid timestamps parsed from filenames.")
        return None
    
    litchi_df = pd.DataFrame({
        "filename": litchi_files,
        "timestamp": timestamps
    })
    litchi_df["timestamp_utc"] = pd.to_datetime(litchi_df["timestamp"]).dt.tz_localize("America/Santiago").dt.tz_convert("UTC")

    #Return the closest litchi file if the timedelta betwwen drone and litchi files are less than 20 minutes
    deltas = np.abs(litchi_df["timestamp_utc"] - drone_tst)

    min_delta = deltas.min()
    if min_delta < time_delta:
        best_match = litchi_df.loc[deltas.idxmin(), "filename"]
        return best_match
    else:
        print(f"[match_litchi_filename] No Litchi file within ({time_delta}) for '{drone.path}'.")
        return None

class PathHandler:

    def __init__(self, num, dirpath=DATADIR):
        self.num = num 
        self.dirpath = dirpath
        self.drone = None
        self.logfile = None
        self.inclino = None
        self.adc = None
        self.gps = None
        self.baro = None
        self.gyro = None
        self.accelero = None
        self.magneto = None
        self.imu_dir = None
        self.litchi = None

    def get_filenames(self, litchi=True):
        
        self.drone = flightpath_from_num(self.num, self.dirpath)
        drone = DJIDrone(self.drone)
        drone.load_data(cols=["GPS:dateTimeStamp"])

        sensors_dir, self.logfile = match_log_filename(drone)

        self.inclino = get_path_from_keyword(sensors_dir, "Kernel-100")
        self.adc = get_path_from_keyword(sensors_dir, "ADS1015")
        self.gps = get_path_from_keyword(sensors_dir, "ZED-F9P")
        self.baro = get_path_from_keyword(sensors_dir, "barometer")
        self.gyro = get_path_from_keyword(sensors_dir, "gyroscope")
        self.accelero = get_path_from_keyword(sensors_dir, "accelerometer")
        self.magneto = get_path_from_keyword(sensors_dir, "magnetometer")

        if litchi:
            self.litchi = match_litchi_filename(drone)

        





        

    
