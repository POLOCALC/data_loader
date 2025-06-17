import os
import datetime

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
    paths = []
    for root, dir, files in os.walk(dirpath):
        for file in files:
            if keyword in file:
                paths.append(os.path.join(root, file))

    if len(paths) == 0:
        print(f"No file found for {keyword}")
        return None
    elif len(paths) == 1:
        paths = paths[0]

    return paths

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