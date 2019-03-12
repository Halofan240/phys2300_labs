'''
Assignment to learn how to interpolate data1
'''
import sys
from datetime import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as ip


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

            # Checks to see if its the initial time
            if is_init_time:
                init_time = recs[1]
                is_init_time = False

            # gets an converts the time to hours, min, secs
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

            # gets an converts the time to hours, min, secs
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

    # Creates a linear line of times from 0 to max gps time then interp1d altitude into it
    x = np.linspace(0, harbor_data["gps_times"][-1], num=len(harbor_data["wx_times"]))
    inter_altitude = ip.interp1d(harbor_data["gps_times"], harbor_data["gps_altitude"], fill_value="extrapolate")
    wx_alt = inter_altitude(x)

    # initial variables for below
    current_alt = 0
    current_temp = 0
    pos = 0

    # Loops through wx_alt and separates the values into increasing altitude and decreasing altitude
    for i in wx_alt:
        if i > current_alt:
            harbor_data["alt_up"].append(i)
            harbor_data["temp_up"].append(harbor_data["wx_temperatures"][pos])
            current_temp = harbor_data["wx_temperatures"][pos]
            current_alt = i
        elif i < current_alt and harbor_data["wx_temperatures"][pos] <= current_temp + 10:
            harbor_data["alt_down"].append(i)
            harbor_data["temp_down"].append(harbor_data["wx_temperatures"][pos])
            current_temp = harbor_data["wx_temperatures"][pos]
            current_alt = i
        pos += 1

    """
    Below is my attempt at trying to correct the graph with correct values
    """

    # i_count = 0
    # j_count = 0
    # current_alt = 0
    # for i in harbor_data["wx_times"]:
    #
    #     for j in harbor_data["gps_times"]:
    #         if i == j:
    #             if harbor_data["gps_altitude"][j_count] >= current_alt:
    #                 harbor_data["alt_up"].append(harbor_data["gps_altitude"][j_count])
    #                 harbor_data["temp_up"].append(harbor_data["wx_temperatures"][i_count])
    #                 current_alt = harbor_data["gps_altitude"][j_count]
    #             elif harbor_data["gps_altitude"][j_count] <= current_alt:
    #                 harbor_data["alt_down"].append(harbor_data["gps_altitude"][j_count])
    #                 harbor_data["temp_down"].append(harbor_data["wx_temperatures"][i_count])
    #                 current_alt = harbor_data["gps_altitude"][j_count]
    #         j_count += 1
    #     i_count += 1
    #     j_count = 0
    #
    # x1 = np.linspace(min(harbor_data["alt_up"]), max(harbor_data["alt_up"]), num=len(harbor_data["wx_temperatures"]), endpoint=True)
    # x2 = np.linspace(min(harbor_data["alt_down"]), max(harbor_data["alt_down"]), num=len(harbor_data["wx_temperatures"]), endpoint=True)
    #
    # for i in harbor_data["wx_temperatures"]:
    #     pass
    #
    # interp_up = ip.interp1d(harbor_data["alt_up"], harbor_data["temp_up"], fill_value="extrapolate")
    # interp_down = ip.interp1d(harbor_data["alt_down"], harbor_data["temp_down"], fill_value="extrapolate")
    #
    #
    #
    # harbor_data["temp_up"] = interp_up(x1)
    # harbor_data["temp_down"] = interp_down(x2)
    # harbor_data["alt_up"] = x1
    # harbor_data["alt_down"] = np.flip(x2)


def match_time(harbor_data):
    """
    Use to match the temperature time with the gps time
    :param harbor_data: A dictionary to collect data.
    :return:
    """
    gps_max_hour = harbor_data["gps_times"][len(harbor_data["gps_times"]) - 1]
    count = 0

    # loops through and sets the the temperature time to match gps time
    for t in harbor_data["wx_times"]:
        if t > gps_max_hour:
            del harbor_data["wx_times"][count:]
            del harbor_data["wx_temperatures"][count:]
        count += 1


def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """

    # Contains the graph for the first part of the assignment
    fig1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex="all")
    ax1.set_title("Harbor Flight Data")
    ax1.plot(harbor_data["wx_times"], harbor_data["wx_temperatures"], "b-")
    ax1.set_ylabel("Temperature, F")
    ax1.set_yticks(np.arange(-60, 100, step=20))

    ax2.set_ylabel("Altitude, ft")
    ax2.set_xlabel("Mission Elapsed Time, Hours")
    ax2.plot(harbor_data["gps_times"], harbor_data["gps_altitude"], "b-")
    ax2.set_xlim(0, 2.5)

    # Contains the graph for the second part of assignment
    fig2, (ax3, ax4) = plt.subplots(nrows=1, ncols=2)
    ax3.set_ylabel("Altitude, ft")
    ax3.set_xlabel("temp")
    ax3.plot(harbor_data["temp_up"], harbor_data["alt_up"], "b-")
    a#x3.set_xlim(-40, 80)
    ax3.set_xticks(np.arange(-40, 100, 20))

    ax4.set_xlabel("temp")
    ax4.plot(harbor_data["temp_down"], harbor_data["alt_down"], "b-")
    #ax4.set_xlim(-60, 120)
    ax4.set_xticks(np.arange(-60, 120, 20))
    # ax4.invert_yaxis()

    plt.show()  # display plot

    """
    Bellow is my attempt to fix graph with correct values
    """
    # ax3.set_ylabel("Altitude, ft")
    # ax3.set_xlabel("Temperature, F")
    # ax3.plot(harbor_data["temp_up"], harbor_data["alt_up"], "b-")
    #ax3.set_xticks(np.arange(-40, 100, 20))
    #
    # ax4.set_xlabel("Temperature, F")
    # ax4.plot(harbor_data["temp_down"], harbor_data["alt_down"], "b-")
    #ax4.set_xticks(np.arange(-60, 120, 20))
    #
    #plt.show()  # display plot


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
    match_time(harbor_data)  # matches time between gps and temp
    interpolate_wx_from_gps(harbor_data)  # calculate interpolated data
    plot_figs(harbor_data)  # display figures


if __name__ == '__main__':
    main()
    sys.exit(0)
