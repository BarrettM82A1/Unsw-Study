## import modules here 
import pandas as pd
import numpy as np
import helper

################# Question 1 #################

# you can call helper functions through the helper module (e.g., helper.slice_data_dim0)
def read_data(filename):
    df = pd.read_csv(filename, sep='\t')
    return (df)
def buc_rec_optimized(df):# do not change the heading of the function
    result =[]
    check =[]
    if df.shape[0] == 1:
        return cal_single_tuple(df)
    elif df.shape[0] > 1:
        result_list = cal_mul_tuple(df,result,check)
        return pd.DataFrame(result, columns=list(df.columns)) 
def cal_single_tuple(df):
    result =[]
    numbers = 2**(len(df.columns)-1)
    for i in range(numbers):
        temp1=[]
        check_bit_string = str_check(df,i)
        for j in range(len(check_bit_string)):
            if check_bit_string[j] == '1':
                temp1.append("ALL")
            else:
                temp1.append(df.values[0][j])
        temp1.append(df.values[0][-1])
        result.append(temp1)
    return pd.DataFrame(result, columns=list(df.columns))                
def cal_mul_tuple(df,result,check):
    dims= df.shape[1]
    check_trace= copy_list(check)
    if dims == 1:
        # only the measure dim
        input_sum = sum( helper.project_data(df, 0) )
        check_trace.append(input_sum)
        result.append(check_trace)
    else:
        # the general case
        dim0_vals = set(helper.project_data(df, 0).values)
        for dim0_v in dim0_vals:
            check_trace.append(dim0_v)
            sub_data = helper.slice_data_dim0(df, dim0_v)
            cal_mul_tuple(sub_data,result,check_trace)
            check_trace = copy_list(check)
        ## for R_{ALL}
        sub_data = helper.remove_first_dim(df)
        check_trace.append('ALL')
        cal_mul_tuple(sub_data,result,check_trace)
    return result
def str_check(df,i):
    a = '0'*(len(df.columns)-1)
    i = bin(i).replace('0b','')
    if len(i) < len(a):
        result ='0'*(len(a)-len(i))+i
    else:
        result = i
    return result
def copy_list(L):
    return [i for i in L]

################# Question 2 #################

def v_opt_dp(x, num_bins):# do not change the heading of the function
    matrix =[]
    bin_list =[]
    for rows in range(num_bins):
            matrix.append(['']*len(x))
            bin_list.append(['']*len(x))           
    for i in range(1,num_bins+1): 
        for j in range(len(x)-1,-1,-1):
            prefix = x[0 : j]
            suffix = x[j : ]
            if i > len(suffix) or len(prefix) < (num_bins - i) :
                cost = -1
                result_matrix = -1 
            elif i == 1 or i == len(suffix):
                result_matrix = suffix
                if i==1:
                    cost = sse(suffix)
                elif i == len(suffix):
                    cost = 0
            else :
                 all_possibles = combine(suffix,i)
                 cost,result_matrix = dealing_target(all_possibles)
            matrix[i-1][j] = cost
            bin_list[i-1][j] = result_matrix
    return matrix,bin_list[i-1][0]
def dealing_target(target_list):
    cost_result = []
    for i in range(len(target_list)):
        cost = calculate_cost(target_list[i])
        cost_result.append(cost)
    min_cost = min(cost_result)
    min_bin_list = target_list[cost_result.index(min_cost)]
    return min_cost,min_bin_list
def calculate_cost(target_list):
    cost=0
    for i in range(len(target_list)):
        cost += sse(target_list[i])
    return cost
def combine(suffix,bins):
    result_list =[]
    def all_combination(target):
        for i in range(1, len(target)):
            for element in all_combination(target[i:]):
                yield [target[:i]] + element
        yield [target]
    all_result = all_combination(suffix)
    for result in all_result:
        if bins == len(result):
            result_list.append(result)
    return result_list
                            
def sse(arr):
    if len(arr) == 0: # deal with arr == []
        return 0.0
    avg = np.average(arr)
    val = sum( [(x-avg)*(x-avg) for x in arr] )
    return val
