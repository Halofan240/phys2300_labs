import math


def Catalan():
    return math.factorial(2 * n) // (math.factorial(n + 1) * math.factorial(n))


n = 0

while Catalan() < pow(10, 9):
    if n == 0:
        print("The %d number in the Catalan series is %d" % (n, Catalan()))
        n += 1
    else:
        print("The %d number in the Catalan series is %d" % (n, Catalan()))
        n += 1
print("Done!")
