# Computes the number of trailing 0's of 1000!
#
# Written by Eric Martin for COMP9021

from math import factorial


n = 1000
x = factorial(n)
nb_of_trailing_0s = 0
while x % 10 == 0:
    nb_of_trailing_0s += 1
    x //= 10
print('There are {} trailing 0s in {}!.'.format(nb_of_trailing_0s, n))
