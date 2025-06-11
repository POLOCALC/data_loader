import os
import numpy as np
import pandas as pd
import datetime
from tools import read_log_time

def match_litchi_filename(drone_cat, litchi_dir="/home/tsouverin/polocalc/data/local/litchi_flightlogs/"):    
    """
    Match and retrieve the file path for a Litchi flight log file based on
    the drone data timestamp.

    Parameters
    ----------
    drone_cat : pandas.DataFrame
        DataFrame containing the drone data with a "GPS:dateTimeStamp" column.
    litchi_dir : str, optional
        Directory where Litchi flight log files are stored.

    Returns
    -------
    str or None
        Path to the matched Litchi file if found, or None if no match is found.
    """
    drone_tst = pd.to_datetime(drone_cat["GPS:dateTimeStamp"].iloc[0])

    #Look for litchi files with matching datetime
    files = [f for f in os.listdir(litchi_dir) if f.endswith("_v2.csv") and f.startswith("20")]

    if not files:
        print("No files found.")
        return None

    #Look for the closest litchi datetime to the drone data
    litchi_data = pd.DataFrame({
        "filename": files,
        "timestamp": [datetime.datetime.strptime(f, "%Y-%m-%d_%H-%M-%S_v2.csv") for f in files]
    })
    
    litchi_data["timestamp_utc"] = pd.to_datetime(litchi_data["timestamp"]).dt.tz_localize("America/Santiago").dt.tz_convert("UTC")

    #Return the closest litchi file if the timedelta betwwen drone and litchi files are less than 20 minutes
    deltas = np.abs(litchi_data["timestamp_utc"] - drone_tst)

    min_delta = deltas.min()
    if min_delta < pd.Timedelta(minutes=10):
        best_match = litchi_data.loc[deltas.idxmin(), "filename"]
        return os.path.join(litchi_dir, best_match)
    else:
        print("No timing match.")
        return None
    
def match_sensor_filename(drone_cat, sensors_root_dir, keyphrase, filename_prefix, max_time_diff=pd.Timedelta(minutes=10)):
    """
    Generic function to match and retrieve a sensor data file based on
    the drone data timestamp.

    Parameters
    ----------
    drone_cat : pandas.DataFrame
        DataFrame containing the drone data with a "GPS:dateTimeStamp" column.
    sensors_root_dir : str
        Root directory where sensor log files are stored.
    keyphrase : str
        Unique log line used to identify the sensor start time.
    filename_prefix : str
        Prefix of the sensor data file.
    max_time_diff : pd.Timedelta
        Maximum time difference allowed for matching.

    Returns
    -------
    matched_file_path : str or None
        Path to the matched sensor data file.
    logfile : str or None
        Path to the logfile from which the file was derived.
    """
    drone_tst = pd.to_datetime(drone_cat["GPS:dateTimeStamp"], utc=True)[0]

    matched_timestamps = []
    matched_files = []
    matched_logs = []

    for root, _, files in os.walk(sensors_root_dir):
        if "file.log" in files:
            logfile = os.path.join(root, "file.log")
            sensors_dir = os.path.join(root, "sensors_data")
            if not os.path.isdir(sensors_dir):
                continue

            sensor_files = [f for f in os.listdir(sensors_dir) if f.startswith(filename_prefix)]
            if not sensor_files:
                continue

            tst = read_log_time(keyphrase=keyphrase, logfile=logfile)
            if tst is None:
                continue

            matched_timestamps.append(pd.to_datetime(tst, utc=True))
            matched_files.append(os.path.join(sensors_dir, sensor_files[0]))
            matched_logs.append(logfile)

    if not matched_timestamps:
        return None, None

    deltas = [abs(t - drone_tst) for t in matched_timestamps]
    min_delta = min(deltas)

    if min_delta <= max_time_diff:
        idx = deltas.index(min_delta)
        return matched_files[idx], matched_logs[idx]
    else:
        return None, None
    
def match_inclino_filenames(drone_cat, sensors_root_dir="/home/tsouverin/polocalc/data/local/payload_data"):
    return match_sensor_filename(
        drone_cat,
        sensors_root_dir,
        keyphrase="Sensor Kernel-100 started",
        filename_prefix="Kernel"
    )

def match_adc_filenames(drone_cat, sensors_root_dir="/home/tsouverin/polocalc/data/local/payload_data"):
    return match_sensor_filename(
        drone_cat,
        sensors_root_dir,
        keyphrase="Sensor ADS1015 started",
        filename_prefix="ADS1015"
    )

def match_gps_filenames(drone_cat, sensors_root_dir="/home/tsouverin/polocalc/data/local/payload_data"):
    return match_sensor_filename(
        drone_cat,
        sensors_root_dir,
        keyphrase="Sensor ZED-F9P started",
        filename_prefix="ZED-F9P"
    )

# def match_inclino_filenames(drone_cat, sensors_root_dir="/home/tsouverin/polocalc/2024_12_campaign"):
#     """
#     Match and retrieve the file path for an inclinometer data file based on
#     the drone data timestamp.

#     Parameters
#     ----------
#     drone_cat : pandas.DataFrame
#         DataFrame containing the drone data with a "GPS:dateTimeStamp" column.
#     sensors_root_dir : str, optional
#         Root directory where sensor log files are stored.

#     Returns
#     -------
#     inclino_path : str or None
#         Path to the matched inclinometer file if found, or None if no match is found.
#     logfile : str or None
#         Path to the logfile from which the matching inclinometer file was derived,

#         or None if no matches are found.
#     """
#     #Load all log files
#     logfiles = [os.path.join(root, "file.log") for root, _, files in os.walk(sensors_root_dir) if "file.log" in files]

#     #Fetch timestamps in log files and corresponding inclinometer filenames
#     inclino_tst = []
#     inclino_files = []
#     return_logfiles = []
#     for logfile in logfiles:
#         f = open(logfile, "r")
#         lines = f.readlines()
#         if len(lines) > 0:
#             sensors_dir = os.path.join(os.path.dirname(logfile), "sensors_data")
#             sensors_files = [file for file in os.listdir(sensors_dir)]
#             is_inclino_file = [f for f in sensors_files if f.startswith("Kernel")]
#             if len(is_inclino_file) > 0:
#                 tst = read_log_time(keyphrase="Sensor Kernel-100 started", logfile=logfile)
#                 inclino_tst.append(tst) 
#                 inclino_files.append(os.path.join(sensors_dir, os.path.join(sensors_dir, is_inclino_file[0])))
#                 return_logfiles.append(logfile)
#     #Return the closest inclinometer file if the timedelta betwwen drone and litchi files are less than 20 minutes
#     drone_tst = pd.to_datetime(drone_cat["GPS:dateTimeStamp"], utc=True)[0]
#     delta_t = ([pd.to_datetime(tst, utc=True) - drone_tst for tst in inclino_tst])
#     if np.abs(np.array(delta_t)).min() < pd.Timedelta(minutes=10):
#         drone_tst = pd.to_datetime(drone_cat["GPS:dateTimeStamp"], utc=True)[0]
#         match_file = np.abs(np.array(delta_t)).argmin()
#         inclino_path = inclino_files[match_file]
#         logfile = return_logfiles[match_file]
#     else:
#         inclino_path = None
#         logfile = None
#     return inclino_path, logfile

# def match_adc_filenames(drone_cat, sensors_root_dir="/home/tsouverin/polocalc/2024_12_campaign"):
#     """
#     Match and retrieve the file path for an ADC data file based on
#     the drone data timestamp.

#     Parameters
#     ----------
#     drone_cat : pandas.DataFrame
#         DataFrame containing the drone data with a "GPS:dateTimeStamp" column.
#     sensors_root_dir : str, optional
#         Root directory where sensor log files are stored.

#     Returns
#     -------
#     adc_path : str or None
#         Path to the matched ADC file if found, or None if no match is found.
#     logfile : str or None
#         Path to the logfile from which the matching ADC file was derived,
#         or None if no matches are found.
#     """
#     #Load all log files
#     logfiles = [os.path.join(root, "file.log") for root, _, files in os.walk(sensors_root_dir) if "file.log" in files]

#     #Fetch timestamps in log files and corresponding gps filenames
#     adc_tst = []
#     adc_files = []
#     return_logfiles = []
#     for logfile in logfiles:
#         f = open(logfile, "r")
#         lines = f.readlines()
#         if len(lines) > 0:
#             sensors_dir = os.path.join(os.path.dirname(logfile), "sensors_data")
#             sensors_files = [file for file in os.listdir(sensors_dir)]
#             is_adc_file = [f for f in sensors_files if f.startswith("ADS1015")]
#             if len(is_adc_file) > 0:
#                 tst = read_log_time(keyphrase="Sensor ADS1015 started", logfile=logfile)
#                 adc_tst.append(tst) 
#                 adc_files.append(os.path.join(sensors_dir, os.path.join(sensors_dir, is_adc_file[0])))
#                 return_logfiles.append(logfile)

#     #Return the closest adc file if the timedelta between drone and adc files are less than 20 minutes
#     drone_tst = pd.to_datetime(drone_cat["GPS:dateTimeStamp"], utc=True)[0]
#     delta_t = ([pd.to_datetime(tst, utc=True) - drone_tst for tst in adc_tst])
#     if np.abs(np.array(delta_t)).min() < pd.Timedelta(minutes=10):
#         match_file = np.abs(np.array(delta_t)).argmin()
#         adc_path = adc_files[match_file]
#         logfile = return_logfiles[match_file]
#     else:
#         adc_path = None
#         logfile = None
#     return adc_path, logfile

# def match_gps_filenames(drone_cat, sensors_root_dir="/home/tsouverin/polocalc/2024_12_campaign"):
#     """
#     Match and retrieve the file path for a GPS data file based on
#     the drone data timestamp.

#     Parameters
#     ----------
#     drone_cat : pandas.DataFrame
#         DataFrame containing the drone data with a "GPS:dateTimeStamp" column.
#     sensors_root_dir : str, optional
#         Root directory where sensor log files are stored.

#     Returns
#     -------
#     gps_path : str or None
#         Path to the matched GPS file if found, or None if no match is found.
#     logfile : str or None
#         Path to the logfile from which the matching GPS file was derived,
#         or None if no matches are found.
#     """    
#     #Load all log files
#     logfiles = [os.path.join(root, "file.log") for root, _, files in os.walk(sensors_root_dir) if "file.log" in files]

#     #Fetch timestamps in log files and corresponding gps filenames
#     gps_tst = []
#     gps_files = []
#     return_logfiles = []
#     for logfile in logfiles:
#         f = open(logfile, "r")
#         lines = f.readlines()
#         if len(lines) > 0:
#             sensors_dir = os.path.join(os.path.dirname(logfile), "sensors_data")
#             sensors_files = [file for file in os.listdir(sensors_dir)]
#             is_gps_file = [f for f in sensors_files if f.startswith("ZED-F9P")]
#             if len(is_gps_file) > 0:
#                 tst = read_log_time(keyphrase="Sensor ZED-F9P started", logfile=logfile)
#                 gps_tst.append(tst) 
#                 gps_files.append(os.path.join(sensors_dir, os.path.join(sensors_dir, is_gps_file[0])))
#                 return_logfiles.append(logfile)

#     #Return the closest inclinometer file if the timedelta between drone and gps files are less than 20 minutes
#     drone_tst = pd.to_datetime(drone_cat["GPS:dateTimeStamp"], utc=True)[0]
#     delta_t = ([pd.to_datetime(tst, utc=True) - drone_tst for tst in gps_tst])
#     if np.abs(np.array(delta_t)).min() < pd.Timedelta(minutes=10):
#         match_file = np.abs(np.array(delta_t)).argmin()
#         gps_path = gps_files[match_file]
#         logfile = return_logfiles[match_file]
#     else:
#         gps_path = None
#         logfile = None
#     return gps_path, logfile

def get_filenames(drone_data, sensors_root_dir="/home/tsouverin/polocalc/data/local/paylod_data", litchi_dir="/home/tsouverin/polocalc/data/local/litchi_flightlogs/"):
    """
    Match and retrieve file paths for litchi, inclinometer, ADC, and GPS data
    based on the drone data timestamp.

    Parameters
    ----------
    drone_data : pandas.DataFrame
        DataFrame containing the drone data with a "GPS:dateTimeStamp" column.
    sensors_root_dir : str, optional
        Root directory where sensor log files are stored.
    litchi_dir : str, optional
        Directory where litchi flight log files are stored.

    Returns
    -------
    litchi_path : str
        Path to the matched litchi file or None if no match is found.
    inclino_path : str
        Path to the matched inclinometer file or None if no match is found.
    adc_path : str
        Path to the matched ADC file or None if no match is found.
    gps_path : str
        Path to the matched GPS file or None if no match is found.
    logfile : str
        Path to the logfile from which the matching files were derived, or
        None if no matches are found.
    """

    litchi_path = match_litchi_filename(drone_data, litchi_dir=litchi_dir)
    inclino_path, logfile1 = match_inclino_filenames(drone_data, sensors_root_dir=sensors_root_dir)
    adc_path, logfile2 = match_adc_filenames(drone_data, sensors_root_dir=sensors_root_dir)
    gps_path, logfile3 = match_gps_filenames(drone_data, sensors_root_dir=sensors_root_dir)

    if logfile1 != logfile2:
        print("Inclinometer and ADC files do not match")
    if logfile2 != logfile3:
        print("ADC and GPS files do not match")
    if logfile2 != logfile3:
        print("Inclinometer and GPS files do not match")

    if logfile1 is not None:
        logfile = logfile1
    elif logfile2 is not None:  
        logfile = logfile2
    elif logfile3 is not None:
        logfile = logfile3
    else:
        logfile = None

    return litchi_path, inclino_path, adc_path, gps_path, logfile