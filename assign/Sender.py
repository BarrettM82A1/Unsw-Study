import sys
# the format:
# python sender.py receice_host_ip receive_port file.txt MWS MSS timeout
# pdrop seed
import math
import random
import Header
from socket import *
import time as timer
import threading
import PLD

#this is input arguments:
receive_host_ip = sys.argv[1]
receive_port = int(sys.argv[2])
file_name = sys.argv[3]
mws =int(sys.argv[4])
mss = int(sys.argv[5])
time_out = float(float(sys.argv[6])/1000) 
pdrop = float(sys.argv[7])
seed_num = int(sys.argv[8])
random.seed(seed_num);
soc = socket(AF_INET,SOCK_DGRAM)
address = (receive_host_ip,receive_port)
logfile = "Sender_log.txt"
soc.settimeout(0.01)
seq =random.randint(0,200)
ack =0
next_seq=0
next_ack = 0
init_time = timer.time()


n_bytes=0
n_seg = 0
n_drop = 0
n_re = 0
n_Du = 0
result1 = ''
def file_buffer(file_name):
    target_file = open(file_name,"r")
    file_buffer = target_file.read()
    target_file.close()
    return file_buffer
def burffer_size(mws,mss):
    return int(mws/mss)
def retransmit_data(re_seq,re_ack,num,target_file,index,n_re,n_bytes):
    for i in range(1):
        head = Header.create_h(re_seq,re_ack,0,0,0,0,2)
        data = head + ' ' + target_file[index:index+num]
        Header.log(data,'snd',logfile,float(timer.time() - init_time))
        soc.sendto(data.encode(),address)

        recv_data,addr = soc.recvfrom(2048)
        rcv_seq, rcv_ack = Header.seq_n(recv_data.decode()),Header.ack_n(recv_data.decode())
        Header.log(recv_data.decode(),'rcv',logfile,float(timer.time() - init_time))
        

def print_info(n_bytes,n_seg,n_drop,n_re,n_Du,result1):
    result1 += "Amount of Data Transferred: " + str(n_bytes)+ '\n'
    result1 += "Number of Data Segments sent " + str(n_seg)+ '\n'
    result1 += "Amount of drop: " + str(n_drop)+ '\n'
    result1 += "Amount of Retransmitted: " + str(n_re)+ '\n'
    output = open(logfile,'a+')
    output.write(result1)
    output.close()
    return output
def three_way_handshake(soc,address,seq,ack,n_seg):
    s_header = Header.create_h(seq,ack,1,0,0,0,1)
    soc.sendto(s_header.encode(),address)
    Header.log(s_header,'snd',logfile,float(timer.time() - init_time))
    check = 0
    n_seg += 1
    while(check == 0):
        try:
            data, addr = soc.recvfrom(2048)
            Header.log(data.decode(),'rcv',logfile,float(timer.time() - init_time))
            
            rcv_seq,rcv_ack = Header.seq_n(data.decode()),Header.ack_n(data.decode())
            next_seq = seq + 1
            next_ack = rcv_seq + 1
            s_header = Header.create_h(next_seq,next_ack,0,1,0,0,1)
            soc.sendto(s_header.encode(),address)
            Header.log(s_header,'snd',logfile,float(timer.time() - init_time))
            seq = next_seq
            ack = next_ack 
            check = 1
            n_seg += 1
        except timeout:
            check = 0
    return seq,ack,n_seg        
    
def sender(soc,address,file_name, mws,mss,seq,ack,n_bytes,n_seg,n_drop,n_re):
    target_file = file_buffer(file_name)
    total_length = len(target_file)
    drop_flag = 0
    num = min(mws,mss)
    current_seq = seq
    current_ack = ack
    next_seq = 0
    next_ack = 0
    seq_check = seq
    final = 0
    index = 0
    re_seq = 0
    while (current_seq - seq < total_length):
        drop_flag = PLD.PLD_check(pdrop)
        if(drop_flag == 0):# do not drop
            try:
                header = Header.create_h(current_seq,current_ack,0,0,0,0,2)
                data  =  header +' '+target_file[index:index + num]
                data2 = target_file[index:index + num]
                soc.sendto(data.encode(), address)
                Header.log(data,"snd", logfile,float(timer.time() - init_time))
                n_seg+=1
                n_bytes += len(data2)
                recv_data,addr = soc.recvfrom(2048)
                rcv_seq, rcv_ack = Header.seq_n(recv_data.decode()),Header.ack_n(recv_data.decode())
                Header.log(recv_data.decode(),'rcv',logfile,float(timer.time() - init_time))
                seq_check += num
                index += num
                next_seq = rcv_ack
                next_ack = rcv_seq
                current_seq = next_seq
                current_ack = next_ack
            except timeout:
                print("nothing sent")
        elif(drop_flag == 1):
            try:
                head = Header.create_h(current_seq,current_ack,0,0,0,drop_flag,2)
                data = head + ' ' + target_file[index:index+num]
                data2= target_file[index:index+num]
                Header.log(data,'drop', logfile,float(timer.time() - init_time))
                soc.sendto(data.encode(), address)
                n_drop += 1
                n_seg+=1
                re_seq = current_seq
                re_ack = current_ack
                re_index = index 
                recv_data,addr = soc.recvfrom(500)
                rcv_seq,rcv_ack = Header.seq_n(recv_data.decode()), Header. ack_n(recv_data.decode())
                Header.log(recv_data.decode(),'rcv',logfile,float(timer.time() - init_time))
                next_seq = rcv_ack + len(data2)
                next_ack = rcv_seq
                current_seq = next_seq
                current_ack = next_ack
                t1 = threading.Timer(time_out,retransmit_data,[re_seq,re_ack,num,target_file,re_index,n_re,n_bytes])
                t1.setDaemon(True)
                t1.start()
            
                index += num
                n_re +=1
                n_bytes += num
                timer.sleep(1.1*time_out)
            except timeout:
                print("111")
    return current_seq,current_ack,n_bytes,n_seg,n_drop,n_re         
   
def close(soc,address,seq,ack,n_seg):
     s_header = Header.create_h(seq,ack,0,0,1,0,3)
     soc.sendto(s_header.encode(),address)
     Header.log(s_header,'snd',logfile,float(timer.time() - init_time))
     n_seg +=1
     check = 0
     while check ==0:
        try:
            data, addr = soc.recvfrom(2048)
            Header.log(data.decode(),'rcv',logfile,float(timer.time() - init_time))
            rcv_seq,rcv_ack = Header.seq_n(data.decode()),Header.ack_n(data.decode())
        
            next_seq = seq + 1
            next_ack = rcv_seq + 1
            s_header = Header.create_h(next_seq,next_ack,0,1,0,0,4)
            soc.sendto(s_header.encode(),address)
            Header.log(s_header,'snd',logfile, float(timer.time() - init_time))
            n_seg +=1
            check = 1
            seq =next_seq
            ack =next_ack
            return seq,ack,n_seg
        except timeout:
            check = 0
Header.clear_log(logfile)
seq,ack,n_seg = three_way_handshake(soc,address,seq,ack,n_seg)
seq,ack,n_bytes,n_seg,n_drop,n_re = sender(soc,address,file_name, mws,mss,seq,ack,n_bytes,n_seg,n_drop,n_re)
seq,ack,n_seg=close(soc,address,seq,ack,n_seg)
print_info(n_bytes,n_seg,n_drop,n_re,n_Du,result1)


