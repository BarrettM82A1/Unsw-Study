# Prompts the user for a strictly positive integer N,
# generates a list of N random integers between 0 and 99, prints out the list,
# computes the number of elements equal to 0, 1, 2 3 modulo 4, and prints these numbers out.
#
# Written by Eric Martin for COMP9021

from random import randint
from sys import exit


nb_of_elements = input('How many elements do you want to generate? ')
try:
    nb_of_elements = int(nb_of_elements)
except ValueError:
    print('Input is not an integer, giving up.')
    exit()
if nb_of_elements <= 0:
    print('Input should be striclty positive, giving up.')
    exit()
L = [randint(0, 99) for _ in range(nb_of_elements)]
print('The list is:' , L)
zero_modulo_4 = 0        
one_modulo_4 = 0
two_modulo_4 = 0
three_modulo_4 = 0
for i in range(nb_of_elements):
    if L[i] % 4 == 0:
        zero_modulo_4 += 1
    elif L[i] % 4 == 1:
        one_modulo_4 += 1
    elif L[i] % 4 == 2:
        two_modulo_4 += 1
    else:
        three_modulo_4 += 1
if zero_modulo_4 < 2:
    print(' There is {} element equal to 0 modulo 4.'.format(zero_modulo_4))
else:
    print(' There are {} elements equal to 0 modulo 4.'.format(zero_modulo_4))
if one_modulo_4 < 2:
    print(' There is {} element equal to 1 modulo 4.'.format(one_modulo_4))
else:
    print(' There are {} elements equal to 1 modulo 4.'.format(one_modulo_4))
if two_modulo_4 < 2:
    print(' There is {} element equal to 2 modulo 4.'.format(two_modulo_4))
else:
    print(' There are {} elements equal to 2 modulo 4.'.format(two_modulo_4))
if three_modulo_4 < 2:
    print(' There is {} element equal to 3 modulo 4.'.format(three_modulo_4))
else:
    print(' There are {} elements equal to 3 modulo 4.'.format(three_modulo_4))
