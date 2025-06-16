import os
import datetime
from pathlib import Path
def read_log_time(keyphrase, logfile):
    """
    Read a log file and find the line containing the given keyphrase.
    Return the timestamp extracted from this line.

    Parameters
    ----------
    keyphrase : str
        The string to search in the log file.
    logfile : str
        Path to the log file.

    Returns
    -------
    tstart : datetime.datetime
        The timestamp extracted from the log file.
    """
    with open(logfile, "r") as f:
        lines = f.readlines()
    
    line_tstart = [line for line in lines if keyphrase in line]
    if len(line_tstart) != 0:
        tstart =  datetime.datetime.strptime(line_tstart[0].split("[")[0].replace(" ", ""), "%Y/%m/%d%H:%M:%S.%f")
        return tstart
    else:
        return None

def drop_nan_and_zero_cols(df):
    """
    Drop any columns in the given DataFrame that consist entirely of NaN or zero values.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to be cleaned.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with any columns consisting of entirely NaN or zero values removed.
    """
    all_nan = df.isna().all()
    all_zero = df.eq(0).all()
    to_drop = all_nan | all_zero
    return df.loc[:, ~to_drop]

def get_path_from_keyword(dirpath, keyword):
    for root, dir, files in os.walk(dirpath):
        for file in files:
            if keyword in file:
                return os.path.join(root, file)
    print(f"No file found for {keyword}")
    return None

def find_flight_path(num, dir_path="/home/tsouverin/polocalc/data/dji_log_data/"):
    """
    Find the path to a flight log file with a given number.

    Parameters
    ----------
    num : int
        The number of the flight log to find.
    dir_path : str
        The root directory to search in. Defaults to
        ``/home/tsouverin/polocalc/data/dji_log_data/``.

    Returns
    -------
    str or None
        The path to the file if found, or ``None`` if the file is not found.
    """
    for root, _, _ in os.walk(dir_path):
        if os.path.isfile(os.path.join(root, f"FLY{num}.csv")):
            return os.path.join(root, f"FLY{num}.csv")
    return None 

def get_logpath_from_datapath(datapath):
    dirname = Path(self.path).resolve().parents[1]
    logpath = str(files[0]) if (files := [f for f in dirname.iterdir() if f.name.startswith("file.log")]) else None
    return logpath

def is_ascii_file(file_bytes):
    """
    Checks if a given file is written in ASCII.

    Parameters
    ----------
    file_bytes : bytes
        Bytes from the file to be checked.

    Returns
    -------
    is_ascii : bool
        True if the file is written in ASCII, False otherwise.
    """
    try:
        file_bytes.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False

def far_to_celcius(temp):
    return (temp - 32)*5/9