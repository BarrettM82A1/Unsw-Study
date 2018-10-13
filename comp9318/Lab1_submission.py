## import modules here
import math
import re
################# Question 0 #################
def add(a, b): # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x): # do not change the heading of the function
    low_position=0
    high_position=x
    EPSILON_q1 = 1E-7
    max_counter_q1 = 1
    half_guess=(high_position + low_position)/2
    while (abs(half_guess**2 - x ) > EPSILON_q1 ) and (max_counter_q1 <= 1000): 
        if half_guess**2 < x:
            low_position = half_guess
        else:
            high_position = half_guess
        half_guess = (low_position + high_position)/2
        max_counter_q1 += 1
    if (1-(half_guess - int(half_guess))) < EPSILON_q1:
         return int(half_guess + 1)
    else:
        return int(half_guess)
################# Question 2 #################

'''
x_0: initial guess
EPSILON: stop when abs(x - x_new) < EPSILON
MAX_ITER: maximum number of iterations

NOTE: you must use the default values of the above parameters, do not change them
'''
def fprime(x):
    return 1.0 + math.log(x)
def f(x):   
    return x * math.log(x) - 16.0
def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    error = 1
    iter_count = 0
    while (error > EPSILON) and (iter_count <= MAX_ITER):
            x = x_0 - (f(x_0)/fprime(x_0))
            error = abs((x - x_0)/x_0)
            iter_count += 1
            x_0 = x
    return  x


################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
def myfind(s, char):
    pos = s.find(char)
    if pos == -1: # not found
        return len(s) + 1
    else: 
        return pos

def next_tok(s): # returns tok, rest_s
    if s == '': 
        return (None, None)
    # normal cases
    poss = [myfind(s, ' '), myfind(s, '['), myfind(s, ']')]
    min_pos = min(poss)
    if poss[0] == min_pos: # separator is a space
        tok, rest_s = s[ : min_pos], s[min_pos+1 : ] # skip the space
        if tok == '': # more than 1 space
            return next_tok(rest_s)
        else:
            return (tok, rest_s)
    else: # separator is a [ or ]
        tok, rest_s = s[ : min_pos], s[min_pos : ]
        if tok == '': # the next char is [ or ]
            return (rest_s[:1], rest_s[1:])
        else:
            return (tok, rest_s)
        
def str_to_tokens(str_tree):
    # remove \n first
    str_tree = str_tree.replace('\n','')
    out = []
    
    tok, s = next_tok(str_tree)
    while tok is not None:
        out.append(tok)
        tok, s = next_tok(s)
    return out

def make_tree(tokens): # do not change the heading of the function
    name = tokens[0]
    child = []
    list_temp = []
    level = 0
    for i in range(2, len(tokens) - 1):
        list_temp.append(tokens[i])
        if tokens[i] == '[':
            level += 1
        elif tokens[i] == ']':
            level -= 1
        if level == 0:
            if tokens[i] == ']' or i+1 >= len(tokens)-1 or tokens[i+1] != '[':
                child.append(make_tree(list_temp))
                list_temp.clear()
    t = Tree(name, child)
    return t

def print_tree(root, indent=0):
    print(' ' * indent, root)
    if len(root.children) > 0:
        for child in root.children:
            print_tree(child, indent+4)            
    
def max_depth(root): # do not change the heading of the function
     return 1+max((max_depth(c) for c in root.children), default=0)
