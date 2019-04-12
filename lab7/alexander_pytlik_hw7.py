import argparse
import csv
import sys

import numpy as np
from vpython import *


def parse_data(infile):
    planet_mass = []
    planet_pos = {'x': [], 'y': [], 'z': []}
    planet_vel = {'vx': [], 'vy': [], 'vz': []}

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
            planet_vel['vx'].append(float(line[4]))
            planet_vel['vy'].append(float(line[5]))
            planet_vel['vz'].append(float(line[6]))

        return planet_mass, planet_pos, planet_vel


def main():
    parser = argparse.ArgumentParser(description='2-Body System Demo')

    parser.add_argument('--pos1', type=str, help='--pos1 x,y,z #Au', default="0,0,0")
    parser.add_argument('--pos2', type=str, help='--pos2 x,y,z #Au', default="5,30,0")
    parser.add_argument('--mass1', type=str, help='--mass1 5.97*10^24 #Kg', default="5.97*10^24")
    parser.add_argument('--mass2', type=str, help='--mass2 1.99*10^30 #Kg', default="1.99*10^30")
    parser.add_argument('--file', help='--file data.cvs')

    args = parser.parse_args()

    planet_mass, planet_pos, planet_vel = parse_data(args.file)

    # x1, y1, z1 = map(float, args.pos1.split(','))
    # x2, y2, z2 = map(float, args.pos2.split(','))
    #
    # mass1 = eval(args.mass1.replace('^', '**'))
    # mass2 = eval(args.mass2.replace('^', '**'))

    tscale = 250
    sizescale = 2
    radscale = 1000
    G = 1.36 * 10 ** -34

    objects = np.empty(len(planet_mass), sphere)
    colors = [color.yellow, color.red, color.blue, color.green, color.orange, color.purple, color.cyan]

    i = 0
    c = 0
    while i < len(planet_mass):
        x, y, z = map(float, (planet_pos['x'][i], planet_pos['y'][i], planet_pos['z'][i]))
        xv, yv, zv = map(float, (planet_vel['vx'][i], planet_vel['vy'][i], planet_vel['vz'][i]))

        objects[i] = sphere(pos=vector(x, y, z), velocity=vector(xv, yv, zv),
                            radius=.25, mass=planet_mass[i], color=colors[c])

        if c == len(colors) - 1:
            c = 0
        else:
            c += 1

        i += 1

    t = 0.0
    dt = 0.01
    tmax = 3.15e+7
    while t < tmax:
        rate(10)

        for i in objects:
            i.acceleration = vector(0, 0, 0)
            for j in objects:
                if i != j:
                    r12 = j.pos - i.pos
                    modr12 = sqrt(r12.x ** 2 + r12.y ** 2 + r12.z ** 2)
                    i.acceleration += G * j.mass * r12 / modr12

        for i in objects:
            i.velocity += i.acceleration * dt
            i.pos += i.velocity * dt

        t += dt

    # t = 0.0
    # while t < tmax:
    #     rate(30)
    #
    #     t += deltat / 30
    #
    #     x = earth_distance * cos(2*pi*t/orbit)
    #     y = earth_distance * sin(2*pi*t/orbit)
    #     earth.pos = vector(x, y, 0)


if __name__ == "__main__":
    main()
    sys.exit(0)
