import sys
import time

import numpy as np
from matplotlib import pyplot as plt
from vpython import *

g = 9.81    # m/s**2
l = 0.1     # meters
W = 0.002   # arm radius
R = 0.01     # ball radius
framerate = 100
steps_per_frame = 10


def set_scene():
    """
    Set Vpython Scene
    :return: Returns the pendulum to be change
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

    # Set background: floor, table, etc
    pivot = vector(0, .075, 0)

    # Creates the ceiling
    ceiling = box(pos=pivot,
                  size=vector(.1, .025, .1),
                  color=color.gray(.5))

    # Creates the ball
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


def f(r):
    """
    Pendulum
    """
    theta = r[0]
    omega = r[1]
    ftheta = omega
    fomega = -(g/l)*np.sin(theta)
    return np.array([ftheta, fomega], float)


def main():
    # Set up initial values
    h = 1.0/(framerate * steps_per_frame)
    r = np.array([np.pi*179/180, 0], float)
    # Initial x and y
    x = l*np.sin(r[0])
    y = -l*np.cos(r[0])

    # Stores the values of theta and the time interval for task 1
    xpoints = []
    tpoints = []

    # Creates Ceiling, Rope, and Ball
    rod, bob = set_scene()

    # Loop over some time interval
    dt = 0.01
    t = 0

    while t < 100:
        # Use the 4'th order Runga-Kutta approximation
        # for i in range(steps_per_frame):
        rate(100)

        # Use the 4'th order Runga-Kutta approximation
        #        for i in range(steps_per_frame):
        r += h * f(r)

        xpoints.append(x)
        tpoints.append(t)
        t += dt

        # Update positions
        x = l * np.sin(r[0])
        y = -l * np.cos(r[0])

        # Update the cylinder axis
        # Update the pendulum's bob
        bob.pos = vector(x, rod.pos.y - y, 0)
        rod.axis = bob.pos - rod.pos

    # Task 1
    plt.plot(tpoints, xpoints)
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.show()


if __name__ == "__main__":
    main()
    time.sleep(10)
    sys.exit(0)
