from vpython import *

x = 2.5
y = -2
z = 10
L = 20
H = .5
W = 18
legRadius = .5/2

table = box(pos=vector(x, y, z),
            axis=vector(radians(90),0,radians(90)),
            size=vector(L, H, W),
            color=color.green)

leg1 = cylinder(pos=vector(15.25,y,10.75), axis=vector(0,5,0), radius=legRadius, color=color.white)
leg2 = cylinder(pos=vector(1.75,-2,-2.75), axis=vector(0,5,0), radius=legRadius, color=color.white)
leg3 = cylinder(pos=vector(3.25,-2,22.75), axis=vector(0,5,0), radius=legRadius, color=color.white)
leg4 = cylinder(pos=vector(-10.25,-2,9.25), axis=vector(0,5,0), radius=legRadius, color=color.white)