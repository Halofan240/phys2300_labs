import sys
import time

import numpy as np
from matplotlib import pyplot as plt
from vpython import *

g = 9.81  # m/s**2
l = 0.1  # meters
W = 0.002  # arm radius
R = 0.01  # ball radius
framerate = 100
steps_per_frame = 10


def set_scene():
    """
    Set Vpython Scene
    :return: Returns the bob and rod to be change
    """
    scene.title = "Assignment 6: Pendulum"
    scene.width = 800
    scene.height = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, .3, -2)
    scene.x = -1

    # Set background: Ceiling, bob, and rod

    # Pivot point of the pendulum
    pivot = vector(0, 0, 0)

    # Creates the ceiling
    ceiling = box(pos=pivot,
                  size=vector(.1, .025, .1),
                  color=color.gray(.5))

    # Creates the bob
    bob = sphere(pos=pivot - vector(0, l, 0),
                 radius=R,
                 color=color.red)

    # Creates the rod
    rod = cylinder(pos=pivot,
                   axis=bob.pos - pivot,
                   radius=W,
                   length=l,
                   color=color.blue)

    return rod, bob


def f(r, t):
    """
    Sets the angular position and acceleration
    :param r: holds the current vector state
    :param t: the current time
    :return: returns the theta and acceleration
    """
    theta = r[0]
    omega = r[1]
    ftheta = omega
    fomega = -((g / l) * np.sin(theta) + .5 * omega)
    return np.array([ftheta, fomega], float)


def rk4(r, t, dt):
    """
    rung kutta 4 function
    :param r: Contains the current vector state
    :param t: Current time
    :param dt: Amount ot increment current time
    :return: returns the results of th rung kutta 4
    """
    k1 = dt * f(r, t)
    k2 = dt * f(r + 0.5 * k1, t + 0.5 * dt)
    k3 = dt * f(r + 0.5 * k2, t + 0.5 * dt)
    k4 = dt * f(r + k3, t + dt)
    return r + (k1 + 2 * k2 + 2 * k3 + k4) / 6, t + dt


def main():
    # Set up initial values
    r = np.array([np.pi * 179 / 180, 0], float)  # Theta = 179
    # r = np.array([np.pi*79 / 180, 0], float)  # Theta = 79
    # r = np.array([np.pi*20/180, 0], float)  # Theta = 20
    theta_title = r[0] * 180 / np.pi  # Title of current plot theta

    # Initial x and y
    x = l * np.sin(r[0])
    y = -l * np.cos(r[0])

    # Stores the values of theta and the time interval for task 1
    xpoints = []
    tpoints = []

    # Creates Ceiling, Rope, and Ball
    rod, bob = set_scene()

    # Loop over some time interval
    dt = 0.01
    t = 0

    while t < 25:
        # Sets the framerate
        rate(framerate)

        # Use the 4'th order Runga-Kutta approximation
        r, t = rk4(r, t, dt)

        # Update positions
        # x = l * np.sin(r[0])
        # y = rod.pos.y - l * np.cos(r[0])
        x = l * np.sin(r[0])
        y = rod.pos.y - l * np.cos(r[0])

        # Stores the position and time for plot
        xpoints.append(x)
        tpoints.append(t)

        # Update the cylinder axis
        # Update the pendulum's bob
        bob.pos = vector(x, y, 0)
        rod.axis = bob.pos - rod.pos
        t = t + dt

    # Plots the pendulum
    plt.plot(tpoints, xpoints)
    plt.title("Theta = %d" % theta_title)
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.show()


if __name__ == "__main__":
    main()
    time.sleep(10)
    sys.exit(0)
