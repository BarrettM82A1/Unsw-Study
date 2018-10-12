# A circular jail has 100 cells numbered from 1 to 100.
# Each cell has an inmate and the door is locked.
# One night the jailor gets drunk and starts running around the jail in circles.
# In his first round he opens each door.
# In his second round he visits every 2nd door (2, 4 , 6, ...) and shuts the door.
# In the 3rd round he visits every 3rd door (3, 6, 9, ...) and if the door is shut
# he opens it, while if it is open then he shuts it.
# This continues for 100 rounds and exhausted the jailor falls down.
# Outputs how many prisoners found their doors open after 100 rounds.
#
# Written by Eric Martin for COMP9021


# After the first round, all doors are open.
# We use index i to refer to door number i.
doors = [True] * 101

for round_nb in range(2, 101):
    for i in range(round_nb, 101, round_nb):
        doors[i] = not doors[i]

print('{} prisoners find their doors open after 100 rounds.'.format(
                           sum(doors[i] for i in range(1, 101) if doors[i])))
    
 
