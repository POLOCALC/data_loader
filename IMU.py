import pandas as pd
from tools import get_path_from_keyword

class IMUSensor:
    def __init__(self, dirpath, keyword):
        self.path = get_path_from_keyword(dirpath, keyword)
        self.data = None

    def load_data(self):
        self.data = pd.read_csv(self.path)

class IMU:
    def __init__(self, dirpath):
        self.dirpath = dirpath
        self.barometer = IMUSensor(dirpath, "barometer.bin")
        self.accelerometer = IMUSensor(dirpath, "accelerometer.bin")
        self.gyroscope = IMUSensor(dirpath, "gyroscope.bin")
        self.magnetometer = IMUSensor(dirpath, "magnetometer.bin")

    def load_all(self):
        for sensor in vars(self).values():
            sensor.load_data()
