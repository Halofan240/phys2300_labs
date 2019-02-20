"""
--------------------------------------------------------------------------------
G e n e r a l I n f o r m a t i o n
--------------------------------------------------------------------------------
Name: weather.py

Usage: python datafile

Description: Code to analyze weather data

Inputs: name of data file containing weather data

Outputs: plots and analysis

Author: Alexander Pytlik

"2/8/2019" - "2/19/2019"

Weber State University
Phys 2300 - Spring 2019

--------------------------------------------------------------------------------
"""

import calendar as cal

import matplotlib.pylab as plt
import numpy as np


def convert_date(date):
    """
    Used to convert the date string into year, month, and day
    :param date:
        Contains the date to separate
    :return:
        Returns the year, month and day in separate values
    """

    year = date[0:4]  # Stores the year
    month = cal.month_abbr[int(date[4:6].lstrip("0"))]  # Converts to abbreviated month name and stores it
    day = date[6:8]  # Stores the day

    return year, month, day


def get_max_min(years, weather_max, weather_min):
    """
    Finds the Max and Min temp of each year
    :param years:
        A list that contains the years for each temp
    :param weather_max:
        Contains the max temp for each day
    :param weather_min:
        Contains the min temp for each day
    :return:
        Returns the 3 list contains the max, min, and year for each year
    """

    year = []  # Holds a single instance of each year that has max and min temps
    max_temp = []  # Holds the Max temp for each year
    min_temp = []  # Holds the Min temp for each year

    # Sets default values for year, max, min, and count
    current_year = years[0]
    current_max = weather_max[0]
    current_min = weather_min[0]
    count = 0

    # Loops through year and grabs the Max and Min temp of that year and stores it
    for y in years:
        if current_year != y:
            year.append(current_year)
            max_temp.append(current_max)
            min_temp.append(current_min)

            current_year = y
            current_max = weather_max[count]
            current_min = weather_min[count]

        if current_max < weather_max[count] != 9999.9:
            current_max = weather_max[count]

        if current_min > weather_min[count] != 9999.9:
            current_min = weather_min[count]

        count += 1

    return year, max_temp, min_temp


def parse_data(infile):
    """
    Function to parse weather data
    :param infile: weather data input file
    :return: two lists. One list with the information from the third column (date)
                        One list with the information from the fourth column (temperature)
    """
    weather_dates = []  # list of dates data
    weather_temp = []  # list of temperature data
    weather_max = []  # list of max temperature data
    weather_min = []  # list of min temperature data

    # Opens file for reading then closes
    with open(infile, mode='r') as file:
        file.readline()  # Removes first line of the file

        # Loops through each line
        for line in file:
            recs = line.split()  # Splits the line into columns
            year, month, day = convert_date(recs[2])
            weather_dates.append(month + " " + day + " " + year)  # Stores the date into a list
            weather_temp.append(float(recs[3]))  # Stores the temp into a list
            weather_max.append(float(recs[17]))  # Stores the max temp into a list
            weather_min.append(float(recs[18]))  # Stores the min temp into a list

    return weather_dates, weather_temp, weather_max, weather_min  # Returns all four list


def calc_mean_std_dev(weather_dates, weather_temp):
    """
    Calculate the mean temperature per month
    Calculate the standard deviation per month's mean
    :param weather_dates: dictionary with dates fields
    :param weather_temp: temperature per month
    :return: means, std_dev: months_mean and std_dev lists
    """

    # Dictionary List of month means data
    month = {"Jan": [], "Feb": [], "Mar": [], "Apr": [], "May": [], "Jun": [],
             "Jul": [], "Aug": [], "Sep": [], "Oct": [], "Nov": [], "Dec": []}

    # List of each month standard deviation and mean data
    month_std = {}
    month_mean = {}

    tmp = []  # Temporary array. Used to store temps for each day of a month
    current_date = None  # Sets current date default
    count = 0  # Sets count default

    # Loops though weather_dates and stores the each day temp into correct month
    for date in weather_dates:
        # Checks to see if we switch months. If so store the temps of that month into correct month in the dictionary
        if current_date != date[0:3] + " " + date[7:11]:
            if len(tmp) != 0:
                month[current_date[0:3]].append(sum(tmp) / len(tmp))
                tmp = []  # Clear array for new month

            # Adds new temp of the new month to tmp array and sets current date
            tmp.append(float(weather_temp[count]))
            current_date = date[0:3] + " " + date[7:11]
            count += 1
        else:
            tmp.append(float(weather_temp[count]))  # Stores the temp of the day for the current month
            count += 1

    # Loops through the Dictionary List and gets the mean and std of each month and stores it
    for key in month:
        month_std[key] = np.std(month.get(key))
        month_mean[key] = sum(month[key]) / len(month[key])

    del tmp  # Deletes temp array

    return month_mean, month_std


def plot_data_task1(wyear, wtemp, month_mean, month_std):
    """
    Create plot for Task 1.
    :param: wyear: list with year (in decimal)
    :param: wtemp: temperature per
    :param: month_mean: list with month's mean values
    :param: month_std: list with month's mean standard dev values
    """

    # Create canvas with two subplots
    plt.figure()
    plt.subplot(2, 1, 1)  # select first subplot
    plt.title("Temperatures at Ogden")
    l = plt.plot(wyear, wtemp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Decimal Year")
    plt.xlim(1970, 2015)
    plt.ylim(-20, 100)
    plt.setp(l, markerfacecolor='C0')

    plt.subplot(2, 1, 2)  # select second subplot
    plt.ylabel("Temperature, F")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.7, 13])
    plt.ylim([0, 90])
    width = 0.8
    plt.bar(monthNumber, month_mean, yerr=month_std, width=width,
            color="lightgreen", ecolor="black", linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.yticks(np.arange(0, 100, 10))
    plt.show()  # display plot


def plot_data_task2(year, max_temp, min_temp):
    """
    Creates a plot of the Max and Min temperature of each year
    :param year:
        Contains a list of each year that has a max and min temp
    :param max_temp:
        Contains a list of the max temp of each year
    :param min_temp:
        Contains a list of the min temp of each year
    :return:
    """
    plt.figure()
    plt.title("High and Low Temperature of Each Year")
    p1 = plt.plot(year, max_temp, "ro")
    p2 = plt.plot(year, min_temp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Year")
    plt.legend((p1[0], p2[0]), ('Maximum Temp', 'Minimum Temp'), loc='lower right')
    plt.show()


def main(infile):
    weather_data = infile  # take data file as input parameter to file

    # Grabs the dates, temp, max temp , and min temp from file
    weather_dates, weather_temp, weather_max, weather_min = parse_data(weather_data)
    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(weather_dates, weather_temp)

    years = []  # An array to contain the years from weather_dates

    # Loops through weather_dates and grabs the years and stores them
    for y in weather_dates:
        years.append(float(y[7:11]))

    # Grabs the Max temp and Min temp of each year
    year, max_temp, min_temp = get_max_min(years, weather_max, weather_min)

    # Plots the data for task 1 and 2
    plot_data_task1(years, weather_temp, list(month_mean.values()), list(month_std.values()))
    plot_data_task2(year, max_temp, min_temp)


if __name__ == "__main__":
    # infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    infile = input("Please enter in the location and name of the weather data file: ")
    main(infile)
    exit(0)
