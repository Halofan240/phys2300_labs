from vpython import *
from math import sin, cos
import argparse
import sys
import time as t


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

    # Set initial velocity & position
    ball_nd.velocity = vector(20, data['init_velocity'], 0)  # Ball velocity
    ball_nd.pos = vector(-25, data['init_height'], 0)  # Ball position

    time = 0  # Starting Time
    force = data['ball_mass'] * data['gravity']  # Force of ball
    acceleration = vector(0, force / data['ball_mass'], 0)  # Acceleration of ball

    # Animate
    while ball_nd.pos.y >= 0:
        rate(1000)

        ball_nd.velocity = ball_nd.velocity + acceleration * data['deltat']
        ball_nd.pos = ball_nd.pos + ball_nd.velocity * data['deltat']

        time += data['deltat']










def motion_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    pass


def main():
    """
    PS G:> python .\lab5\lab5.py --help
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

    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
    #     motion_drag(data)
    # 4) Plot Information: extra credit
    #     plot_data(data)


if __name__ == "__main__":
    main()
    t.sleep(10)
    sys.exit(0)