'''
Assignment to learn how to interpolate data1
'''
import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pandas as pd
from datetime import datetime as dt


# https://youtu.be/-zvHQXnBO6c


def read_wx_data(wx_file, harbor_data):
    """
    Read temperature and time data from file.
    Populates the harbor_data dictionary with two lists: wx_times and wx_temperatures
    :param wx_file: File object with data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    harbor_data["wx_times"] = []
    harbor_data["wx_temperatures"] = []

    # Opens file for reading then closes
    with open(wx_file, mode='r') as file:
        file.readline()  # Removes first line of the file

        init_time = None
        is_init_time = True

        # Loops through each line
        for line in file:
            recs = line.split(',')  # Splits the line into columns

            if is_init_time:
                init_time = recs[1]
                is_init_time = False

            delta_t = dt.strptime(recs[1], '%H:%M:%S') - dt.strptime(init_time, '%H:%M:%S')  # get delta time
            harbor_data['wx_times'].append(float(delta_t.total_seconds() / 3600))  # convert to hours
            harbor_data["wx_temperatures"].append(float(recs[3]))


def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    harbor_data["gps_times"] = []
    harbor_data["gps_altitude"] = []

    # Opens file for reading then closes
    with open(gps_file, mode='r') as file:
        file.readline()  # Removes first line of the file
        file.readline()  # Removes second line of the file

        init_time = None
        is_init_time = True

        # Loops through each line
        for line in file:
            recs = line.split()  # Splits the line into columns

            if is_init_time:
                init_time = ":".join(recs[0:3])
                is_init_time = False

            # get delta time
            delta_t = dt.strptime(":".join(recs[0:3]), '%H:%M:%S') - dt.strptime(init_time, '%H:%M:%S')
            harbor_data['gps_times'].append(float(delta_t.total_seconds() / 3600))  # convert to hours
            harbor_data["gps_altitude"].append(int(recs[6]))


def interpolate_wx_from_gps(harbor_data):
    """
    Compute wx altitudes by interpolating from gps altitudes
    Populates the harbor_data dictionary with four lists:
        1) wx correlated altitude up
        2) wx correlated temperature up
        3) wx correlated altitude down
        4) wx correlated temperature down
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    harbor_data["alt_up"] = []
    harbor_data["temp_up"] = []
    harbor_data["alt_down"] = []
    harbor_data["temp_down"] = []

    pass


def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """

    gps_max_hour = harbor_data["gps_times"][len(harbor_data["gps_times"]) - 1]
    count = 0

    for t in harbor_data["wx_times"]:
        if t > gps_max_hour:
            del harbor_data["wx_times"][count:]
            del harbor_data["wx_temperatures"][count:]
        count += 1

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex="all")
    ax1.set_title("Harbor Flight Data")
    ax1.plot(harbor_data["wx_times"], harbor_data["wx_temperatures"], "b-")
    ax1.set_ylabel("Temperature, F")
    ax1.set_yticks(np.arange(-60, 100, step=20))

    ax2.set_ylabel("Altitude, ft")
    ax2.set_xlabel("Mission Elapsed Time, Hours")
    ax2.plot(harbor_data["gps_times"], harbor_data["gps_altitude"], "b-")
    ax2.set_xlim(0, 2.5)
    fig.show()  # display plot


def main():
    """
    Main function
    :return: Nothing
    """
    harbor_data = {}
    wx_file = 'data/TempPressure.txt'
    gps_file = 'data/GPSData.txt'
    # wx_file = sys.argv[1]  # first program input param
    # gps_file = sys.argv[2]  # second program input param

    read_wx_data(wx_file, harbor_data)  # collect weather data
    read_gps_data(gps_file, harbor_data)  # collect gps data
    interpolate_wx_from_gps(harbor_data)  # calculate interpolated data
    plot_figs(harbor_data)  # display figures


if __name__ == '__main__':
    main()
    sys.exit(0)
