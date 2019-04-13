import numpy as np
from vpython import *

# Global Variables
frame_rate = 30
tscale = 250
sizescale = 2
radscale = 1000
nplanets = 2  # two planets
# Params of the planets
#     earth, mercury
orbit = [365.3, 88.0]  # period of object days)
planet_radius = [6371, 2440]  # radisu of object (km)
rad = [149.6, 57.9]  # raidus of orbit (km)
sun_size = 3000.0
# Open graphic window
# display(width=800, height=800)
# Draw Sun
sphere(pos=vector(0, 0, 0), radius=sun_size, color=color.yellow)
# Draw the initial position of the planets
planet = np.empty(nplanets, sphere)
for p in range(nplanets):
    x = radscale * rad[p]
    y = 0.0
    planet[p] = sphere(pos=vector(x, y, 0), radius=sizescale * planet_radius[p], color=color.blue)

# Main loop
t = 0.0
while t < 90000:
    # Next time step
    rate(frame_rate)
    t += tscale / frame_rate
    # Draw  each planet
    for p in range(nplanets):
        x = radscale * rad[p] * cos(2 * pi * t / orbit[p])
        y = radscale * rad[p] * sin(2 * pi * t / orbit[p])
        planet[p].pos = vector(x, y, 0)
