import pandas as pd
from tools import drop_nan_and_zero_cols

class DJIDrone:
    def __init__(self, path):
        self.path = path
        self.data = None

    def load_data(self, cols=None):
        """
        Load and filter drone data from a CSV file.

        The function:
        - Loads only specified columns.
        - Converts 'GPS:dateTimeStamp' to datetime.
        - Filters out rows with missing or zero values in critical columns.
        - Drops any columns that are fully NaN or zero using `drop_nan_and_zero_cols`.

        Parameters
        ----------
        cols : list of str, optional
            List of columns to load. Defaults to key RTK and timestamp fields.

        Returns
        -------
        None
            Filtered data is stored in `self.data`.
        """
        if cols is None:
            cols = ["Clock:offsetTime", 'GPS:dateTimeStamp', "RTKdata:GpsState", "RTKdata:Lat_P", "RTKdata:Lon_P", "RTKdata:Hmsl_P"]

        data = pd.read_csv(self.path, low_memory=False, usecols=cols)
        ind = pd.Series(True, index=data.index)

        if "GPS:dateTimeStamp" in data.columns:
            data["GPS:dateTimeStamp"] = pd.to_datetime(data["GPS:dateTimeStamp"].values, errors="coerce")
            ind &= data["GPS:dateTimeStamp"].notna()
        if "RTKdata:GpsState" in data.columns:
            ind &= data["RTKdata:GpsState"].notna()
        if "RTKdata:Lat_P" in data.columns:
            ind &= data["RTKdata:Lat_P"] != 0  

        data = data[ind].reset_index(drop=True)
        data = drop_nan_and_zero_cols(data)
        
        self.data = data
