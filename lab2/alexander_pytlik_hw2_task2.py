"""
Alexander Pytlik
1/30/2019 - 2/14/2019

Weber State University
Phys 2300 - Spring 2019
Programming Assignment M2
"""

# Import list
import matplotlib.pyplot as plt


# "Main" Function
def main():
    # Gets the user inputs and stores them into a values array
    values = get_user_input()

    # Plots the data onto the graph using the users inputted values
    plot_data(values)


# A function to capture user input
def get_user_input():
    # Ask the user for input and stores it
    x0 = user_input("Horizontal Distance: ")
    vx0 = user_input("Horizontal Velocity: ")
    y0 = user_input("Vertical Distance: ")
    vy0 = user_input("Vertical Velocity: ")

    # Stores the x0, vx0, y0, vy0 into a array and returns it
    values = [x0, vx0, y0, vy0]
    return values


# Used to check if user enter a int.
def user_input(description):
    # Loops until user enters correct value
    while True:
        # Uses try except to determine if user enter correct value
        try:
            return int(input(description))  # Returns user input if the input is a int

        # Throws a exception if user inputted a value that isn't a int
        except ValueError:
            print("Please enter in a number value\n")


# Function to calculate projectile motion
def projectile(x, v, t, a):
    # x = distance, v = velocity, t = time, a = acceleration
    return x + v * t + 0.5 * a * t ** 2  # Formula for projectile motion


# Function to plot data
def plot_data(values):
    delta = 0.1  # Increments time by .1 second or 100 milliseconds
    t = 0.0  # Starting Time
    intervals = 0  # how many times values are added to x and y. Used for the while loop

    ax = 0.0  # constant for horizontal acceleration
    ay = -9.8  # constant for earths gravity

    x = []  # Stores the x projectile values
    y = []  # Stores the y projectile values

    # Basically a do while loop to calculate and store the x and y values
    while True:
        # values[0] = x0, values[1] = vx0, values[2] = y0, values[3] = vy0
        x.append(projectile(values[0], values[1], t, ax))  # Calculates the x value and stores it in x[]
        y.append(projectile(values[2], values[3], t, ay))  # Calculates the y value and stores it in y[]
        t = t + delta  # Increments the time by .1 second or 100 Milliseconds

        # If the new y value is less then 0 then break the loop as the projectile has reach the ground
        if y[intervals] < 0:
            break
        intervals += 1  # Increments how many times we loop

    plt.plot(x, y)  # Plots the x and y values
    plt.show()  # Shows the graph after plotting


if __name__ == "__main__":  # Starts the Main function
    main()
