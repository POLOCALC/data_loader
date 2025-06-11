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
    for root, dir, files in os.walk(dirpath):
        for file in files:
            if keyword in file:
                return os.path.join(root, file)
    print(f"No file found for {keyword}")
    return None
def far_to_celcius(temp):
    return (temp - 32)*5/9