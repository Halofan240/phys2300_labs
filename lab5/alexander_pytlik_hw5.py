import argparse
import sys
import time as t
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos

from vpython import *


def set_scene(data):
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 5: Projectile motion"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1
    # Set background: floor, table, etc


def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    ball_nd = sphere(radius=1, color=color.cyan, make_trail=True)
    # Follow the movement of the ball
    scene.camera.follow(ball_nd)

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

    data['no_drag_x'].append(ball_nd.pos.x)
    data['no_drag_y'].append(ball_nd.pos.y)

    # Animate
    while ball_nd.pos.y >= 0:
        rate(1000)

        ball_nd.velocity = ball_nd.velocity + acceleration * deltat
        ball_nd.pos = ball_nd.pos + ball_nd.velocity * deltat

        data['no_drag_x'].append(ball_nd.pos.x)
        data['no_drag_y'].append(ball_nd.pos.y)

    ft = data['no_drag_y'][-2] / (data['no_drag_y'][-2] - data['no_drag_y'][-1])  # fractional time to last point
    data['no_drag_x'][-1] = data['no_drag_x'][-2] + (data['no_drag_x'][-1] - data['no_drag_x'][-2]) * ft
    data['no_drag_y'][-1] = 0.

    ball_nd.pos.x = data['no_drag_x'][-1]
    ball_nd.pos.y = data['no_drag_y'][-1]


def motion_drag(data):
    """
    Create animation for projectile motion with dragging force
    """
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

    data['with_drag_x'].append(ball_nd.pos.x)
    data['with_drag_y'].append(ball_nd.pos.y)

    # Animate
    while ball_nd.pos.y >= 0:
        rate(1000)

        velocity = sqrt(ball_nd.velocity.x ** 2 + ball_nd.velocity.y ** 2)  # Sets current velocity

        fx = 1 - beta * velocity * deltat  # Force of x
        fy = (-beta * ball_nd.velocity.y * velocity + data['gravity']) * deltat  # Force of y

        ball_nd.velocity.x = ball_nd.velocity.x * fx  # Velocity with drag
        ball_nd.velocity.y = ball_nd.velocity.y + fy  # Velocity with drag

        ball_nd.pos = ball_nd.pos + ball_nd.velocity * deltat  # Updates ball position

        data['with_drag_x'].append(ball_nd.pos.x)
        data['with_drag_y'].append(ball_nd.pos.y)

    ft = data['with_drag_y'][-2] / (data['with_drag_y'][-2] - data['with_drag_y'][-1])  # fractional time to last point
    data['with_drag_x'][-1] = data['with_drag_x'][-2] + (data['with_drag_x'][-1] - data['with_drag_x'][-2]) * ft
    data['with_drag_y'][-1] = 0.

    ball_nd.pos.x = data['with_drag_x'][-1]
    ball_nd.pos.y = data['with_drag_y'][-1]


def plot_data(data):
    plt.figure()

    plt.title("Projectile Motion Data")
    plt.ylabel("Projectile Height, m")
    plt.xlabel("Projectile Distance, m")

    p1 = plt.plot(data["no_drag_x"], data["no_drag_y"], "c-")
    p2 = plt.plot(data["with_drag_x"], data["with_drag_y"], "b-")
    plt.axhline(0, color='black', linestyle='--')
    plt.axvline(-25, color='black', linestyle='--')

    plt.xticks(np.arange(-25, data['no_drag_x'][-1] + 10, 5))
    plt.legend((p1[0], p2[0]), ('No Drag', 'With Drag'), loc='upper right')

    plt.show()  # display plot


def main():
    """
    PS G:> python .\lab5\alexander_pytlik_hw5.py --help
    """
    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description='Projectile Motion Demo')

    parser.add_argument('--velocity', type=float, help='--velocity 20', required=True)
    parser.add_argument('--angle', type=float, help='--angle 45', required=True)
    parser.add_argument('--height', type=float, nargs='?', default=1.2, help='--height 1.2')

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

    data['no_drag_x'] = []
    data['no_drag_y'] = []
    data['with_drag_x'] = []
    data['with_drag_y'] = []

    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
    motion_drag(data)
    # 4) Plot Information: extra credit
    plot_data(data)


if __name__ == "__main__":
    main()
    t.sleep(10)
    sys.exit(0)
