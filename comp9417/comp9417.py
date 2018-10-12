import math
import pickle

def read_data(filename):
    f = open(filename)
    lines = f.readlines()
    dic = {}
    for line in lines:
        data = line.split('\t')
        if data[0] not in dic:
            dic[data[0]] = {}
        dic[data[0]][data[1]] = float(data[2])
    return dic

def get_mean(dic):
    p_mean = 0
    for r in dic:
        p_mean += dic[r]
    p_mean = p_mean/len(dic)
    return p_mean   

def get_NR(required_movie_list):
    result = {}
    max_rate = 5
    min_rate = 1
    
    #for i in range(len(required_movie_list)):
    for key in required_movie_list:
        temp = (2*(required_movie_list[key]-min_rate)- (max_rate - min_rate))/ (max_rate - min_rate)
        result[key] =float(temp)
    return result

def get_R(required_NR_list):
    #result = {}
    max_rate = 5
    min_rate = 1
    R =  0.5*((required_NR_list + 1) * (max_rate - min_rate)) + min_rate

    return R

def Collaborative_filter1(file_path, p_user, p_movie, data, mean_dic):  # Adjust Cosine
    #data = read_data(file_path)
    similarity = {}
    p_mean = get_mean(data[p_user]) #mean value rated by p_user
    p_item = []  #all items rated by p_user
    p_rated = {}
    for key in data[p_user]:
        p_item.append(key)
        p_rated[key] = data[p_user][key]
    simi = {}
    for i in p_item:
        if i == p_movie or i not in p_item:
            continue
        top = 0
        butx = 0
        buty = 0
        for user in data:
            if i in data[user] and p_movie in data[user]:
                mean = get_mean(data[user])
                #print(mean,user)
                top += (data[user][i] - mean)*(data[user][p_movie] - mean)
                butx += (data[user][i] - mean)**2
                buty += (data[user][p_movie] - mean)**2
                #print(data[user][i],data[user][p_movie],user)
        deno = math.sqrt(butx) * math.sqrt(buty)
        if deno != 0:
            simi[i] = top/deno
            #print(math.sqrt(butx))
        else:
            simi[i] = 0
    nr = get_NR(p_rated)
    #print(nr)
    top = 0
    but = 0
    for key in p_rated:
        top += simi[key]*nr[key]
        but += abs(simi[key])
    if but == 0:
        return 0
    else:
        return get_R(top/but)
    

def get_mean_rating(filename):
    f = open(filename)
    lines = f.readlines()
    dic = {}
    for line in lines:
        data = line.split('\t')
        if data[1] not in dic:
            dic[data[1]] = []
        dic[data[1]].append(float(data[2]))
    for key in dic:
        dic[key] = sum(dic[key])/len(dic[key])
    return dic
      
def Collaborative_filter2(file_path, p_user, p_movie, data, mean_dic):  #Pearson Correlation Coefficient
    
    similarity = {}
    p_mean = get_mean(data[p_user]) #mean value rated by p_user
    p_item = []  #all items rated by p_user
    p_rated = {}
    for key in data[p_user]:
        p_item.append(key)
        p_rated[key] = data[p_user][key]
    simi = {}
    
    for i in p_item:
        if i == p_movie or i not in p_item:
            continue
        top = 0
        butx = 0
        buty = 0
        for user in data:
            if i in data[user] and p_movie in data[user]:
                mean1 = mean_dic[i]
                mean2 = mean_dic[p_movie]
                #print(mean,user)
                top += (data[user][i] - mean1)*(data[user][p_movie] - mean2)
                butx += (data[user][i] - mean1)**2
                buty += (data[user][p_movie] - mean2)**2
                #print(data[user][i],data[user][p_movie],user)
        deno = math.sqrt(butx) * math.sqrt(buty)
        if deno != 0:
            simi[i] = top/deno
            #print(math.sqrt(butx))
        else:
            simi[i] = 0
    nr = get_NR(p_rated)
    #print(nr)
    top = 0
    but = 0
    for key in p_rated:
        top += simi[key]*nr[key]
        but += abs(simi[key])
    if but == 0:
        return 0
    else:
        return get_R(top/but)
    
def Collaborative_filter3(file_path, p_user, p_movie, data, mean_dic):  #Tranditional Cosine
    
    similarity = {}
    #p_mean = get_mean(data[p_user]) #mean value rated by p_user
    p_item = []  #all items rated by p_user
    p_rated = {}
    for key in data[p_user]:
        p_item.append(key)
        p_rated[key] = data[p_user][key]
    simi = {}
    
    for i in p_item:
        if i == p_movie or i not in p_item:
            continue
        top = 0
        butx = 0
        buty = 0
        for user in data:
            if i in data[user] and p_movie in data[user]:
                #if i not in data[user]:                    
                #    buty += (data[user][p_movie])**2
                #elif p_movie not in data[user]:
                #    butx += (data[user][i])**2
                #mean1 = mean_dic[i]
                #mean2 = mean_dic[p_movie]
                #print(mean,user)
                #else:
                top += (data[user][i])*(data[user][p_movie])
                butx += (data[user][i])**2
                buty += (data[user][p_movie])**2
                #print(data[user][i],data[user][p_movie],user)
        deno = math.sqrt(butx) * math.sqrt(buty)
        if deno != 0:
            simi[i] = top/deno
            #print(math.sqrt(butx))
        else:
            simi[i] = 0
    nr = get_NR(p_rated)
    top = 0
    but = 0
    for key in p_rated:
        top += simi[key]*nr[key]
        but += abs(simi[key])
    if but == 0:
        return 0
    else:
        return get_R(top/but)    
    
    
def cross_validation():    
    result = 0
    output = open('pearson.dat', 'wb')
    final = []

    for i in range(1,6):
        training_path = './ml-100k/u' + str(i) + '.base'
        testing_path = './ml-100k/u' + str(i) + '.test'
        data = read_data(testing_path)
        mae = 0
        n = 0
        m=0
        mean_dic = get_mean_rating(training_path)
        data1 = read_data(training_path)
        for user in data:
            for movie in data[user]:
                if m % 1== 0.0:
                    predict = Collaborative_filter2(training_path,user,movie,data1,mean_dic)
                    if predict == 0:
                        continue
                    mae += abs(predict - data[user][movie])
                    n += 1
                m+=1
        result += mae/n
        final.append((mae/n,n))
        print(mae/n,training_path,n)
    final.append(result/5)
    pickle.dump(final,output)
    print(result/5)
    
def recommendation(user,num):
    data = read_data('./ml-100k/u.data')
    user_movie = []
    for movie in data[user]:
        user_movie.append(movie)
    mean_dic = get_mean_rating('./ml-100k/u.data')
    all_movie = []
    for movie in mean_dic:
        all_movie.append(movie)
    movie_list = {}
    for movie in all_movie:
        if movie not in user_movie:
            predict = Collaborative_filter3('./ml-100k/u.data', user, movie)
            movie_list[movie] = predict
    recommend_list = []
    for i in range(num):
        m = max(movie_list.items(), key = lambda x:x[1])
        recommend_list.append(m[0])
        movie_list.pop(m[0])
    return recommend_list

#print(recommendation('1',5))

cross_validation()

    
#print(Collaborative_filter('./ml-latest-small/movies.csv', '1', '6'))
