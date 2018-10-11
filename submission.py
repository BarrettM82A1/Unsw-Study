## Submission.py for COMP6714-Project1
import math
class InvertedList:
    def __init__(self, l):
        self.data = l[:] # make a copy
        self.cur = 0     # the cursor 

    def get_list(self):
        return self.data
 
    def eol(self):
        # we use cur == len(list) to indicate EOL
        return False if self.cur < len(self.data) else True
    
    def next(self, val = 1):
        # does not allow cur to be out-of-range, but use len(list) to indicate EOL
        self.cur = min(self.cur + val, len(self.data)) 
            
    def elem(self):
        if self.eol():
            return None
        else: 
            return self.data[self.cur]
    def peek(self, pos):
        # look at the element under the current cursor, but does not advance the cursor. 
        if pos < len(self.data):
            return self.data[pos]
        else:
            return None
    def reset(self):
        self.cur = 0 
###################################################################################################################
## Question No. 0:
def add(a, b): # do not change the heading of the function
    return a + b




###################################################################################################################
## Question No. 1:
def binary_search(array, target):
    lower = 0
    upper = len(array)
    while lower < upper:   
        x = lower + (upper - lower) // 2
        val = array[x]
        if target == val:
            return x
        elif target > val:
            if lower == x:   
                break        
            lower = x
        elif target < val:
            upper = x
    return x+1
def gallop_to(a, val):# do not change the heading of the function
    #stage1:
    bound=1
    pos = 0
    a.reset()
    while (a.cur + pos < len(a.data)) and (a.data[pos] < val):
        temp = pos
        pos = 2**bound - 2 
        bound += 1
    if(a.cur + pos > len(a.data)):
            pos = len(a.data)-1   
    interval_list = a.data[temp:pos+1]
    temp2 = binary_search(interval_list,val)
    a.cur = a.cur + temp + temp2


###################################################################################################################
## Question No. 2:
def merge(a,b):
    a.extend(b)
    return sorted(a)
def logic(token,buffer_size,L,Z,index):
    Z[0] = merge(Z[0],[token])
    if len(Z[0]) == buffer_size:
        i=0
        while True:
            if i in index:
                a = merge(L[i],Z[i])
                if len(Z) > i+1:
                    Z[i+1] = a
                else:
                    Z.append(a)
                del index[i]
            else:
                if len(L) >= len(Z):
                    L[i] = Z[i]
                else:
                    L.append(Z[i])
                index[i] = True
                break
            i+=1
        Z[0] = []

    
def Logarithmic_merge(index, cut_off, buffer_size): # do not change the heading of the function
    execute_list=index[:cut_off]
    L =[[]]
    Z =[[]]
    index={}
    result =[]
    for i in range(len(execute_list)):
        logic(execute_list[i],buffer_size,L,Z,index)
    result.append(Z[0])
    for i in range(len(L)):
        if i in index:
             result.append(L[i])
        else:
             result.append([])
    return result
             
        
    



###################################################################################################################
## Question No. 3:

def decode_gamma(inputs):# do not change the heading of the function
    result = []
    while len(inputs) > 0:
        length = inputs.index('0')
        move_set =inputs[length+1:length*2+1]
        result.append(int("1"+ move_set,2))
        inputs = inputs[length*2+1:]
    return result 

def decode_delta(inputs):# do not change the heading of the function
    result =[]
    while len(inputs) > 0 :
        length = inputs.index('0')
        N_set=inputs[length+1:length*2+1]
        expo = int('1' + N_set,2)-1
        move_set = inputs[length*2+1:length*2+1+expo]
        a = 2**expo + int(move_set,2)
        result.append(a)
        inputs = inputs[length*2+1+expo:]
    return result
        
        

def decode_rice(inputs, b):# do not change the heading of the function
    result = []
    while len(inputs) > 0:
        length  = inputs.index("0")
        r_bit = int(math.log(b,2) )
        move_set = inputs[length+1:length+1+r_bit]
        a = int(move_set,2)+ length*b
        result.append(a)
        inputs = inputs[length+1+r_bit:]
    return result
        
