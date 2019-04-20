import argparse
import sys
import time as t

import matplotlib.pyplot as plt
import numpy as np
from vpython import *


def set_scene(data):
    """
    Set Vpython Scene
    :param data: Contains the constants and x and y coordinates for both drag and no drag
    :return:
    """
    scene.title = "Assignment 8: Projectile motion with bounce"
    scene.width = 800
    scene.height = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1

    # Set background: floor, table, etc
    ball_table = box(pos=vector(-25, data['init_height'] - 1.5, 0),
                     size=vector(4, 1, 4),
                     color=color.red)

    ground_table = box(pos=vector(-2, data['init_height'] - 2.5, 0),
                       size=vector(50, 1, 6),
                       color=color.gray(.5))


def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    :param data: Contains the constants and x and y coordinates for both drag and no drag
    :return:
    """
    # Creates the ball
    ball_nd = sphere(radius=1, color=color.cyan, make_trail=True)

    # Follow the movement of the ball
    scene.camera.follow(ball_nd)

    # Stores the constant values into local variables
    deltat = data['deltat']
    mass = data['ball_mass']
    theta = radians(data['theta'])
    velocity = data['init_velocity']

    # Set initial velocity & position
    ball_nd.velocity = vector(velocity * cos(theta),  # Initial X velocity
                              velocity * sin(theta), 0)  # Initial Y velocity
    ball_nd.pos = vector(-25, data['init_height'], 0)  # Initial ball position
    force = mass * data['gravity']  # Force of ball
    acceleration = vector(0, force / mass, 0)  # Acceleration of ball

    # Animate
    t = 0
    tmax = 10
    while ball_nd.velocity.y >= 0:
        while ball_nd.pos.y >= 0:
            rate(1000)

            # Stores the new x and y values
            data['no_drag_x'].append(ball_nd.pos.x)
            data['no_drag_y'].append(ball_nd.pos.y)

            # Sets the new velocity of the ball and updates the position
            ball_nd.velocity = ball_nd.velocity + acceleration * deltat
            ball_nd.pos = ball_nd.pos + ball_nd.velocity * deltat

        # Get the x value when y = 0 of the projectile
        ft = data['no_drag_y'][-2] / (data['no_drag_y'][-2] - data['no_drag_y'][-1])  # fractional time to last point
        ball_nd.pos.x = data['no_drag_x'][-2] + (data['no_drag_x'][-1] - data['no_drag_x'][-2]) * ft
        ball_nd.pos.y = 0.

        # Appends the final x and y coordinates of no drag
        data['no_drag_x'].append(ball_nd.pos.x)
        data['no_drag_y'].append(ball_nd.pos.y)

        if ball_nd.velocity.y <= 0:
            if ball_nd.velocity.x <= .5 and ball_nd.velocity.y >= -.1:
                break
            ball_nd.velocity.y = -ball_nd.velocity.y
            # ball_nd.pos.y = ball_nd.pos.y + ball_nd.velocity.y

        if t == tmax:
            break

        t += 1


def motion_drag(data):
    """
    Create animation for projectile motion with dragging force
    :param data: Contains the constants and x and y coordinates for both drag and no drag
    :return:
    """

    # Creates the ball
    ball_nd = sphere(radius=1, color=color.blue, make_trail=True)

    # Follow the movement of the ball
    scene.camera.follow(ball_nd)

    # Initial Values
    beta = data['beta']
    deltat = data['deltat']
    theta = radians(data['theta'])
    velocity = data['init_velocity']

    # Set initial velocity & position
    ball_nd.velocity = vector(velocity * cos(theta),  # Initial X velocity
                              velocity * sin(theta), 0)  # Initial Y velocity
    ball_nd.pos = vector(-25, data['init_height'], 0)  # Initial ball position

    # Appends initial x and y to plot
    data['with_drag_x'].append(ball_nd.pos.x)
    data['with_drag_y'].append(ball_nd.pos.y)

    # Animate
    while ball_nd.velocity.y >= 0:
        while ball_nd.pos.y >= 0:
            rate(1000)

            # Formula to add drag to projectile motion
            fx = 1 - beta * velocity * deltat  # Force of x
            fy = (-beta * ball_nd.velocity.y * velocity + data['gravity']) * deltat  # Force of y

            ball_nd.velocity.x = ball_nd.velocity.x * fx  # Velocity with drag
            ball_nd.velocity.y = ball_nd.velocity.y + fy  # Velocity with drag

            # Appends x and y to plot
            data['with_drag_x'].append(ball_nd.pos.x)
            data['with_drag_y'].append(ball_nd.pos.y)

            # Sets new velocity and updates x and y position
            velocity = sqrt(ball_nd.velocity.x ** 2 + ball_nd.velocity.y ** 2)  # Sets current velocity
            ball_nd.pos = ball_nd.pos + ball_nd.velocity * deltat  # Updates ball position

        # Get the x value when y = 0 of the projectile
        ft = data['with_drag_y'][-2] / (
                data['with_drag_y'][-2] - data['with_drag_y'][-1])  # fractional time to last point
        ball_nd.pos.x = data['with_drag_x'][-2] + (data['with_drag_x'][-1] - data['with_drag_x'][-2]) * ft
        ball_nd.pos.y = 0.

        # Appends the final x and y coordinates of no drag
        data['with_drag_x'].append(ball_nd.pos.x)
        data['with_drag_y'].append(ball_nd.pos.y)

        if ball_nd.velocity.y <= 0:
            if ball_nd.velocity.x <= .5 and ball_nd.velocity.y >= -.1:
                break
            ball_nd.velocity.y = -ball_nd.velocity.y
            # ball_nd.pos.y = ball_nd.pos.y + ball_nd.velocity.y


def plot_data(data):
    """
    Plots the no drag and with drag projectile motions
    :param data: Contains the constants and x and y coordinates for both drag and no drag
    :return:
    """
    # Creates plot
    plt.figure()

    # Set titles for plot and x and y
    plt.title("Projectile Motion Data")
    plt.ylabel("Projectile Height, m")
    plt.xlabel("Projectile Distance, m")

    # Adds plots of projectile motion for drag and no drag
    p1 = plt.plot(data["no_drag_x"], data["no_drag_y"], "c-")  # No drag plot
    p2 = plt.plot(data["with_drag_x"], data["with_drag_y"], "b-")  # With drag plot

    # Sets the axis line for x and y
    plt.axhline(0, color='black', linestyle='--')  # Axis horizontal line at 0
    plt.axvline(-25, color='black', linestyle='--')  # Axis at vertical line at -25

    # Sets ticks to no drag plot do to longer distance
    plt.xticks(np.arange(-25, data['no_drag_x'][-1] + 10, 5))

    # Creates legend show which line is what
    plt.legend((p1[0], p2[0]), ('No Drag', 'With Drag'), loc='upper right')

    plt.show()  # display plot


def main():
    """
    PS G:> python .\lab5\alexander_pytlik_hw8.py --help
    """
    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description='Projectile Motion Demo')

    # Grabs the users input for velocity, angle, and height(optional)
    parser.add_argument('--velocity', type=float, default=20, help='--velocity 20')
    parser.add_argument('--angle', type=float, default=45, help='--angle 45')
    parser.add_argument('--height', type=float, default=1.2, help='--height 1.2')

    args = parser.parse_args()

    # Set Variables
    data = {}  # empty dictionary for all data and variables
    data['init_height'] = args.height  # y-axis
    data['init_velocity'] = args.velocity  # m/s
    data['theta'] = args.angle  # degrees

    # Constants
    data['rho'] = 1.225  # kg/m^3
    data['Cd'] = 0.5  # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.8  # m/s^2

    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.075  # meters
    data['ball_area'] = pi * data['ball_radius'] ** 2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / 2.0
    data['beta'] = data['alpha'] / data['ball_mass']

    # Creates 4 list to hold the x and y values for the plot
    data['no_drag_x'] = []  # Holds x no drag values
    data['no_drag_y'] = []  # Holds y no drag values
    data['with_drag_x'] = []  # Holds x with drag values
    data['with_drag_y'] = []  # Holds y with drag values

    # Set Scene
    set_scene(data)

    # 2) No Drag Animation
    # motion_no_drag(data)

    # 3) Drag Animation
    motion_drag(data)

    # Current Doesnt Work
    # 4) Plot Information: extra credit
    # plot_data(data)


if __name__ == "__main__":
    main()
    t.sleep(10)
    sys.exit(0)
