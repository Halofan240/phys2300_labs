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

"2/8/2019" - "Finish Date"

Weber State University
Phys 2300 - Spring 2019

--------------------------------------------------------------------------------
"""

import sys
import calendar as cal
import matplotlib.pylab as plt
import numpy as np


# Pseudocode:
# 1) get the name of the data file from the user on the command line
# 2) open the data file
# 3) read the first line of data and throw it away (it is the header info the computer doesn't need)
#       from all the remaining lines:
#       read in the date (index 2) and temperature (index 3)
#       parse the date string into year, month, day
#       convert year, month, day into decimal years for plotting (this would make a great function!)
#       (need to pay attention to leap years here!)
# 4) make two lists for the time series - the decimal year list and the temperature list
# 5) sort the data by month so we can average it and take the standard deviation later
# 6) Plot the results

def convert_date(date):
    year = date[0:4]
    month = cal.month_abbr[int(date[4:6].lstrip("0"))]
    day = date[6:8]

    return year, month, day


def parse_data(infile):
    """
    Function to parse weather data
    :param infile: weather data input file
    :return: two lists. One list with the information from the third column (date)
                        One list with the information from the fourth column (temperature)
    """
    weather_dates = []  # list of dates data
    weather_temp = []  # list of temperarture data

    # Opens file for reading then closes
    with open(infile, mode='r') as file:
        file.readline()  # Removes first line of the file

        # Loops through each line
        for line in file:
            recs = line.split()  # Splits the line into columns
            year, month, day = convert_date(recs[2])
            weather_dates.append(month + " " + day + " " + year)  # Stores the date into a list
            weather_temp.append(recs[3])  # Stores the temp into a list

    return weather_dates, weather_temp  # Returns both list


def calc_mean_std_dev(weather_dates, weather_temp):
    """
    Calculate the mean temperature per month
    Calculate the standard deviation per month's mean
    :param weather_dates: dictionary with dates fields
    :param weather_temp: temperature per month
    :return: means, std_dev: months_mean and std_dev lists
    """
    month = {"Jan": [], "Feb": [], "Mar": [], "Apr": [], "May": [], "Jun": [],
             "Jul": [], "Aug": [], "Sep": [], "Oct": [], "Nov": [], "Dec": []}  # List of month means data

    # List of each month standard deviation data
    month_std = {}
    month_mean = {}

    tmp = []
    current_date = None
    count = 0

    for date in weather_dates:
        if current_date != date[0:3] + " " + date[7:11]:
            if len(tmp) != 0:
                month[current_date[0:3]].append(sum(tmp)/len(tmp))
                current_date = date[0:3] + " " + date[7:11]
                tmp = []

            tmp.append(float(weather_temp[count]))
            current_date = date[0:3] + " " + date[7:11]
            count += 1
        else:
            tmp.append(float(weather_temp[count]))
            count += 1

    for key in month:
        month_std[key] = np.std(month.get(key))
        month_mean[key] = sum(month[key]) / len(month[key])

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
    plt.plot(wyear, wtemp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Decimal Year")
    plt.xlim(1970, 2015)
    plt.ylim(-20, 100)

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
    plt.show()  # display plot


def plot_data_task2(xxx):
    """
    Create plot for Task 2. Describe in here what you are plotting
    Also modify the function to take the params you think you will need
    to plot the requirements.
    :param: xxx??
    """
    pass


def main(infile):
    weather_data = infile  # take data file as input parameter to file
    weather_dates, weather_temp = parse_data(weather_data)
    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(weather_dates, weather_temp)

    years = []

    for year in weather_dates:
        years.append(int(year[7:11]))

    years = np.asarray(years)
    weather_temp = np.asarray(weather_temp)
    month_mean = np.asarray(list(month_mean.values()))
    month_std = np.asarray(list(month_std.values()))

    plot_data_task1(years, weather_temp, month_mean, month_std)
    # TODO: Create the data you need for this
    # plot_data_task2(xxx)


if __name__ == "__main__":
    infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    # infile = input("Please enter in the location and name of the weather data file: ")
    main(infile)
    exit(0)
