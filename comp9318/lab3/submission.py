## import modules here 
################# Question 1 #################
def multinomial_nb(training_data, sms):# do not change the heading of the function
    tokens=get_freqs_of_tokens(sms)
    cal_ham_num = {}
    cal_spam_num = {}
    cal_voca_num = {}
    cal_1_occ = {}
    cal_2_occ = {}
    ham_num=spam_num=voca_num=0
    num_cal_1 = num_cal_2=num_total=p_cal_1=p_cal_2 =0
    cal_1 = training_data[0][1]
    for i in range(len(training_data)):
        if training_data[i][1] == cal_1:
                num_cal_1 += 1
                for k,v in training_data[i][0].items():
                    if k in cal_ham_num.keys():
                        cal_ham_num[k] += v
                    else:
                        cal_ham_num[k] = v
        if training_data[i][1] != cal_1:
                num_cal_2 += 1
                for k,v in training_data[i][0].items():
                    if k in cal_spam_num.keys():
                        cal_spam_num[k] += v
                    else:
                        cal_spam_num[k] = v
        num_total +=1
        for k,v in training_data[i][0].items():
                if k in cal_voca_num.keys():
                    cal_voca_num[k] += v
                else:
                    cal_voca_num[k] = v
    p_cal_1 = num_cal_1/num_total
    p_cal_2 = num_cal_2/num_total
    for k,v in cal_ham_num.items():
        ham_num += v
    for k,v in cal_spam_num.items():
        spam_num += v
    voca_num = len(cal_voca_num)
    for i,j in tokens.items():
        if i in cal_ham_num.keys():
            cal_1_occ[i] = cal_ham_num[i]
        else:
            cal_1_occ[i] = 0
        if i in cal_spam_num.keys():
            cal_2_occ[i] = cal_spam_num[i]
        else:
            cal_2_occ[i] =0
    p1_list=[]
    p2_list=[]
    p1=p2=0
    alpha = 1
    cal_1_result=1
    cal_2_result=1
    for i,j in cal_1_occ.items():
        if cal_1_occ[i] ==0 and cal_2_occ[i]==0:
            p1_list.append(1)
            p2_list.append(1)
        else:
            p1=(cal_1_occ[i]+alpha)/(ham_num+voca_num)
            p2=(cal_2_occ[i]+alpha)/(spam_num+voca_num)
            p1_list.append(p1)
            p2_list.append(p2)
    for i in range(len(p1_list)):
        cal_1_result = cal_1_result * p1_list[i]
    for i in range(len(p2_list)):
        cal_2_result = cal_2_result * p2_list[i]
    result = (p_cal_2*cal_2_result)/(p_cal_1 * cal_1_result)
    return result
def get_freqs_of_tokens(sms):
    results = {}
    for token in sms:
        if token not in results:
            results[token] = 1
        else:
            results[token] += 1
    return results
