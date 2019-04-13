import argparse
import csv
import sys

import numpy as np
from vpython import *


def parse_data(infile):
    """
    retrieves the planets from the given file.
    :param infile: Contains the data of the planet
    :return: Returns the planets velocity, position and mass
    """

    # Creates arrays to store the values
    planet_mass = []
    planet_pos = {'x': [], 'y': [], 'z': []}
    planet_vel = {'xv': [], 'yv': [], 'zv': []}

    # Opens file for reading then closes
    with open(infile, mode='r') as csv_file:
        csv_file.readline()  # Removes first line of the file
        csv_file.readline()  # Removes second line of the file

        csv_reader = csv.reader(csv_file, delimiter=',')  # Splits the line into columns

        # Loops through each line
        for line in csv_reader:
            planet_mass.append(float(line[7]))
            planet_pos['x'].append(float(line[1]))
            planet_pos['y'].append(float(line[2]))
            planet_pos['z'].append(float(line[3]))
            planet_vel['xv'].append(float(line[4]))
            planet_vel['yv'].append(float(line[5]))
            planet_vel['zv'].append(float(line[6]))

        return planet_mass, planet_pos, planet_vel


def user_input(pos1, pos2, vel1, vel2, mass1, mass2):
    """
    Stores the user input into arrays
    :param pos1: Contains the first planet position
    :param pos2: Contains the second planet position
    :param vel1: Contains the first planet velocity
    :param vel2: Contains the second planet velocity
    :param mass1: Contains the first planet mass
    :param mass2: Contains the second planet mss
    :return: Returns the arrays containing the values
    """

    planet_mass = []
    planet_pos = {'x': [], 'y': [], 'z': []}
    planet_vel = {'xv': [], 'yv': [], 'zv': []}

    # Splits the position and velocity into separate values
    x1, y1, z1 = map(float, pos1.split(','))
    x2, y2, z2 = map(float, pos2.split(','))
    xv1, yv1, zv1 = map(float, vel1.split(','))
    xv2, yv2, zv2 = map(float, vel2.split(','))

    # Planet Position
    planet_pos['x'].append(x1)
    planet_pos['x'].append(x2)
    planet_pos['y'].append(y1)
    planet_pos['y'].append(y2)
    planet_pos['z'].append(z1)
    planet_pos['z'].append(z2)

    # Planet velocity
    planet_vel['xv'].append(xv1)
    planet_vel['xv'].append(xv2)
    planet_vel['yv'].append(yv1)
    planet_vel['yv'].append(yv2)
    planet_vel['zv'].append(zv1)
    planet_vel['zv'].append(zv2)

    # Planet Mass
    planet_mass.append(eval(mass1.replace('^', '**')))
    planet_mass.append(eval(mass2.replace('^', '**')))

    return planet_mass, planet_pos, planet_vel


def planets(objects, planet_mass, planet_pos, planet_vel):
    """
    Creates the planets from the given values
    :param objects: Holds the created planets
    :param planet_mass: Contains the planet mass
    :param planet_pos:  Contains the planets position
    :param planet_vel:  Contains the planets velocity
    :return:
    """

    # Color array. Used to set planet colors
    colors = [color.yellow, color.red, color.blue, color.green, color.orange, color.purple, color.cyan]

    i = 0  # initial start of loop
    c = 0  # initial start of color array
    while i < len(planet_mass):

        # Stores the position into x, y, z and the velocity into xv, yv, zv
        x, y, z = map(float, (planet_pos['x'][i], planet_pos['y'][i], planet_pos['z'][i]))
        xv, yv, zv = map(float, (planet_vel['xv'][i], planet_vel['yv'][i], planet_vel['zv'][i]))

        # Creates a sphere contains the planets data and stores it into objects
        objects[i] = sphere(pos=vector(x, y, z), velocity=vector(xv, yv, zv),
                            radius=.25, mass=planet_mass[i], color=colors[c])

        if c == len(colors) - 1:  # Checks to see if at the end of color array
            c = 0  # if at end start over
        else:
            c += 1  # if not at end go to next part

        i += 1  # increments the objects holder


def euler_cromer(objects, G, dt, tmax):
    """
    Euler-Cromer method for n-body simulation
    :param objects: contains the planets
    :param G: constant value of the galaxy gravity
    :param dt: Contains the time step
    :param tmax: Max time to run the simulation
    :return:
    """

    t = 0.0
    while t < tmax:
        rate(10)

        # Loops through each planet in objects and updates the acceleration
        for i in objects:
            i.acceleration = vector(0, 0, 0)
            for j in objects:
                if i != j:
                    r12 = j.pos - i.pos
                    modr12 = sqrt(r12.x ** 2 + r12.y ** 2 + r12.z ** 2)
                    i.acceleration += G * j.mass * r12 / modr12

        # Updates the velocity and position of the planets
        for i in objects:
            i.velocity += i.acceleration * dt
            i.pos += i.velocity * dt

        t += dt


def leap_frog(objects, G, dt, tmax):
    """
    Leapfrog method for n-body simulation
    :param objects: contains the planets
    :param G: constant value of the galaxy gravity
    :param dt: Contains the time step
    :param tmax: Max time to run the simulation
    :return:
    """

    t = 0.0
    first_step = 0
    while t < tmax:
        rate(10)

        # Loops through each planet in objects and updates the acceleration
        for i in objects:
            i.acceleration = vector(0, 0, 0)
            for j in objects:
                if i != j:
                    r12 = j.pos - i.pos
                    modr12 = sqrt(r12.x ** 2 + r12.y ** 2 + r12.z ** 2)
                    i.acceleration += G * j.mass * r12 / modr12

        # Updates the velocity and position of the planets using leapfrog method
        if first_step == 0:
            for i in objects:
                i.velocity += i.acceleration * (dt / 2)
                i.pos += i.velocity * dt
            first_step = 1
        else:
            for i in objects:
                i.velocity += i.acceleration * dt
                i.pos += i.velocity * dt

        t += dt


def main():
    # Creates argparse name parser
    parser = argparse.ArgumentParser(description='2-Body System Demo')

    parser.add_argument('--pos1', type=str, help='--pos1 x,y,z #Au', default="0,0,0")  # Default sun position
    parser.add_argument('--pos2', type=str, help='--pos2 x,y,z #Au',
                        default="-0.136364695954795,0.893397922857,0.387458344639667")  # Default earth position
    parser.add_argument('--vel1', type=str, help='--vel1 xv,yv,zv #Au', default="0,0,0")  # Default sun velocity
    parser.add_argument('--vel2', type=str, help='--vel2 xv,yv,zv #Au',
                        default="-0.0173199988485296,-0.0022443047317656,-0.000973361115758044")  # Default earth velocity
    parser.add_argument('--mass1', type=str, help='--mass1 5.97*10^24 #Kg', default="1.99e+30")  # Default sun mass
    parser.add_argument('--mass2', type=str, help='--mass2 1.99*10^30 #Kg', default="5.97e+24")  # Default earth mass
    parser.add_argument('--file', help='--file data.cvs')

    args = parser.parse_args()

    # If a file was added grab and store the values
    if args.file:
        planet_mass, planet_pos, planet_vel = parse_data(args.file)
    else:  # If no file was selected
        planet_mass, planet_pos, planet_vel = user_input(args.pos1, args.pos2, args.vel1,
                                                         args.vel2, args.mass1, args.mass2)

    # Creates a objects array of the number of planets
    objects = np.empty(len(planet_mass), sphere)

    G = 1.36e-34  # Galaxy gravity constant
    dt = 1  # timestep
    tmax = 10e+6  # max time for simulation

    planets(objects, planet_mass, planet_pos, planet_vel)  # Creates the planets
    # euler_cromer(objects, G, dt, tmax)  # Euler Method
    leap_frog(objects, G, dt, tmax)  # Leapfrog Method


if __name__ == "__main__":
    main()
    sys.exit(0)
