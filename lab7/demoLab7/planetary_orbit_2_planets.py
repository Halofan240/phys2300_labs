"""
Planetary Orbit of two planets usign the Bulisrsh-Stoer method. 
"""
from math import sqrt
from matplotlib import pyplot as plt
from numpy import empty, array, arange, copy

# Constants
G = 6.6738e-11  # Newton's Gravitational Contant
M = 1.9891e30  # Mass of the Sun (kg)
m = 5.9722e24  # Earth's mass
year = 31557600  # One year in seconds
week = 7 * 24 * 3600  # One week in seconds
delta = 1000 / year

# Earth Params
x0 = 1.5210e11
y0 = 0.0
vx0 = 0.0
vy0 = 2.9291e4
a = 0.0
b = year
H = week


# Function fun(r)
def fun(f):
    x = r[0]
    y = r[1]
    vx = r[2]
    vy = r[3]
    fx = vx
    fy = vy
    fvx = -G * M * x / sqrt(x * x + y * y) ** 3
    fvy = -G * M * y / sqrt(x * x + y * y) ** 3
    return array([fx, fy, fvx, fvy])


xpoints = []
ypoints = []
# Do the "Big Steps" of size H
r = array([x0, y0, vx0, vy0], float)
for t in arange(a, b, H):
    xpoints.append(r[0])
    ypoints.append(r[1])
    # Do the leapfrog step to get things started
    n = 1
    h = H
    r1 = copy(r)
    r2 = r1 + 0.5 * h * fun(r1)
    r1 += h * fun(r2)

    R1 = empty([1, 4], float)
    R1[0] = r1

    # Now increase n and extrapolate
    error = 2 * H * delta
    while abs(error) > H * delta:
        n += 1
        h = H / n
        # Leap frog method
        r1 = copy(r)
        r2 = r1 + 0.5 * h * fun(r1)
        for i in range(n):
            r1 += h * fun(r2)
            r2 += h * fun(r1)

        # Calculate extrapolation estimates
        R2 = R1
        R1 = empty([n, 4], float)
        R1[0] = r1
        for m in range(1, n):
            epsilon = (R1[m - 1] - R2[m - 1]) / ((n / (n - 1)) ** (2 * m) - 1)
            R1[m] = R1[m - 1] + epsilon
            error = sqrt(epsilon[0] ** 2 + epsilon[1] ** 2)
    # Set r equal to the most accurate estimate
    r = R1[n - 1]

# Plot the results
plt.plot(xpoints, ypoints)
print(xpoints, ypoints)
plt.show()
