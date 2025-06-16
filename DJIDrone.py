import pandas as pd
from tools import drop_nan_and_zero_cols

class DJIDrone:
    def __init__(self, path):
        self.path = path
        self.data = None
    def load_data(self):
        """
        Read the drone data from the given CSV file. The function filters the
        data to select only the rows in which both the RTK latitude and the
        computed latitude are valid. The function also filters the data to
        select only the rows in which the RTK latitude refreshed.

        Parameters
        ----------
        datapath : string
            The path to the CSV file containing the drone data.

        Returns
        -------
        drone_data : pandas.DataFrame
            A DataFrame containing the filtered drone data.
        """
        data = pd.read_csv(self.path, low_memory=False, usecols=["Clock:offsetTime", 'GPS:dateTimeStamp', "RTKdata:GpsState", "RTKdata:Lat_P", "RTKdata:Lon_P", "RTKdata:Hmsl_P"])
        ind = data["RTKdata:GpsState"].notna() & data["RTKdata:Lat_P"] != 0 & data["GPS:dateTimeStamp"].notna()
        data = data[ind].reset_index(drop=True)
        data["GPS:dateTimeStamp"] = pd.to_datetime(data["GPS:dateTimeStamp"].values)
        data = drop_nan_and_zero_cols(data)
        self.data = data
