import sys
import socket
import time
import PLD
#this is the header file:

def create_h(seq,ack,syn_flag,ack_flag,fin_flag,drop_flag,status_code):
    return str(seq)+' ' + str(ack) + ' ' +  str(syn_flag) + str(ack_flag)+ str(fin_flag)+str(drop_flag)+' '+ str(status_code) 

def type_p(package):
    flag = package.split(' ',4)[2]
    if (flag == '0000'):
        return "D"
    elif (flag == "1000"):
        return "S"
    elif (flag == '0100'):
        return "A"
    elif (flag == '1100'):
        return "SA"
    elif (flag == '0010'):
        return "F"
    elif (flag == '0110'):
        return "FA"
    elif (flag[3] == '1' ):
        return "D"
def status_n(package):
    return  int(package.split(' ', 4)[3])
def seq_n(package):
    return  int(package.split(' ', 4 )[0])
def ack_n(package):
    return  int(package.split(' ', 4)[1])
def drop_n(package):
    return  int(package.split(' ',4)[2][3])

def NumBytes(package):
    temp = package.split(' ',4)
    if len(temp) == 4:
        return 0
    else:
        return len(temp[4]) 
def clear_log(log_file):
    output = open(log_file,'w')
    output.write("<s/r/d> <time> <type> <seq> <bytes> <ack>"+ '\n')
    output.close()
def clear_file(log_file):
    output = open(log_file,'w')
    output.write('')
    output.close()
def write_log(result,log_file):
    output = open(log_file,'a+')
    output.write(result)
    output.close()
    return output
def log(package,srd,logfile,time_log):
#<snd rcv drop> <time> <type of packet> <seq_num> <number of bytes> <ack_num>
    type_of_pac = type_p(package)
    seq, num_bytes,ack = seq_n(package), NumBytes(package),ack_n(package)
    result = str(srd) + ' ' + str(float("%.3f"%time_log)) + ' ' + str(type_of_pac) + ' '
    result += str(seq) + ' '+ str(num_bytes) + ' '+  str(ack) +'\n'
    logfile = write_log(result, logfile)
