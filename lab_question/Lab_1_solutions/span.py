# Generates a list of 10 random integers between -50 and 50, prints out the list,
# computes the difference between the largest and smallest values in the list,
# and prints it out.
#
# Written by Eric Martin for COMP9021

from random import randint


L = [randint(-50, 50) for _ in range(10)]
print('The list is:' , L)
max_element = -50
min_element = 50
for i in range(10):
    if L[i] > max_element:
        max_element = L[i]
    if L[i] < min_element:
        min_element = L[i]
print('  The maximum difference between largest and smallest values in this list is:',
      max_element - min_element)
print('Confirming with builtin operations:', max(L) - min(L))
