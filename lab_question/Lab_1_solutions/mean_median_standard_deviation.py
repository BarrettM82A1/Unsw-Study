# Prompts the user for a strictly positive integer N,
# generates a list of N random integers between -50 and 50, prints out the list,
# computes the mean, the median and the standard deviation in two ways,
# that is, using or not the functions from the statistics module, and prints them out.
#
# Written by Eric Martin for COMP9021

from random import randint
from sys import exit
from math import sqrt
from statistics import mean, median, pstdev


nb_of_elements = input('How many elements do you want to generate? ')
try:
    nb_of_elements = int(nb_of_elements)
except ValueError:
    print('Input is not an integer, giving up.')
    exit()
if nb_of_elements <= 0:
    print('Input should be striclty positive, giving up.')
    exit()
L = [randint(-50, 50) for _ in range(nb_of_elements)]
print('The list is:' , L)
the_mean = sum(L) / nb_of_elements
the_standard_deviation = sqrt(sum(x ** 2 for x in L) / nb_of_elements - the_mean ** 2)
L.sort()
if nb_of_elements % 2:
    the_median = L[nb_of_elements // 2]
else:
    the_median = (L[(nb_of_elements - 1) // 2] + L[nb_of_elements // 2]) / 2
print('  The mean is {:.2f}.'.format(the_mean))
print('  The median is {:.2f}.'.format(the_median))
print('  The standard deviation is {:.2f}.'.format(the_standard_deviation))
print('Confirming with functions from the statistics module:')
print('  The mean is {:.2f}.'.format(mean(L)))
print('  The median is {:.2f}.'.format(median(L)))
print('  The standard deviation is {:.2f}.'.format(pstdev(L)))
    
