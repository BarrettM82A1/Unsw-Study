import sys
from socket import *
import random
import Header 
import time as timer
#format: python receiver.py receiver_port file.txt
init_time = timer.time()
receiver_port = int(sys.argv[1])
output_file = sys.argv[2]
logfile = 'Receiver_log.txt'
seq = random.randint(0,200)
ack = 0
next_seq = 0
next_ack = 0
buffer ={}
Header.clear_log(logfile)
Header.clear_file(output_file)

n_size = 0
n_seg = 0
def write_output(result):
    output = open(output_file,'a+')
    output.write(result)
    output.close()
    return output
def deal_with_buffer(buffer):
     a=[]
     for k in buffer:
         a.append(k)
     sorted(a)
     for i in range(len(a)):
        write_output(buffer[int(a[i])])
def print_info(n_size, n_seg):
    result = "Amount of Data Received(exclude) Received data : " + str(n_size) + '\n'
    result += 'Number if Data Segments Received(not include retransmit): ' + str(n_seg)
    output = open(logfile,'a+')
    output.write(result)
    output.close()
    
result = ''
address = ('', receiver_port)  
soc = socket(AF_INET,SOCK_DGRAM)  
soc.bind(address)
status = 0
hand_check = True
fin_check = True
re_check = True
num_bytes = 0
buffer = {};
while status < 4 :
    data, addr = soc.recvfrom(2048)
    status = Header.status_n(data.decode())
    drop_flag = Header.drop_n(data.decode())
    Header.log(data.decode(),'rcv',logfile,float(timer.time() - init_time))
    n_seg+=1
    if status == 3:#colse
        if fin_check == True:
            rcv_seq,rcv_ack = Header.seq_n(data.decode()),Header.ack_n(data.decode())
            next_seq = seq
            next_ack = rcv_seq + 1
            pac = Header.create_h(next_seq, next_ack, 0,1,1,0,3)
            Header.log(pac,'snd',logfile,float(timer.time() - init_time))
            soc.sendto(pac.encode(),addr)
            seq = next_seq
            ack = next_ack
            check = False
    elif status == 2:#send_data
        if drop_flag == 0 :
            num_bytes = Header.NumBytes(data.decode())
            rcv_seq,rcv_ack =  Header.seq_n(data.decode()), Header. ack_n(data.decode())
            if(num_bytes != 0):
                 buffer[rcv_seq] = data.decode().split(' ',4)[4]
                 n_size += len(data.decode().split(' ',4)[4])
            next_seq = rcv_ack 
            next_ack = rcv_seq + num_bytes
            pac = Header.create_h(next_seq, next_ack,0,1,0,0,2)
            Header.log(pac,'snd',logfile,float(timer.time() - init_time))
            soc.sendto(pac.encode(),addr)
            seq = next_seq
            ack = next_ack
        elif drop_flag == 1 :
            rcv_seq,rcv_ack =  Header.seq_n(data.decode()), Header. ack_n(data.decode())
            buffer[rcv_seq]=''
            n_size -= len(data.decode().split(' ',4)[4])
            next_seq = rcv_ack
            next_ack = rcv_seq
            num_bytes = Header.NumBytes(data.decode())
            pac = Header.create_h(next_seq, next_ack,0,1,0,0,2)
            Header.log(pac,'snd',logfile,float(timer.time() - init_time))
            soc.sendto(pac.encode(),addr)
            seq = next_seq
            ack = next_ack
            n_seg -= 1
    elif status == 1 :#hand_shake
         if hand_check == True:
            rcv_seq,rcv_ack = Header.seq_n(data.decode()),Header.ack_n(data.decode())
            next_seq = seq
            next_ack = rcv_seq + 1
            pac = Header.create_h(next_seq, next_ack, 1,1,0,0,1)
            Header.log(pac,'snd',logfile,float(timer.time() - init_time))
            soc.sendto(pac.encode(),addr)
            seq = next_seq
            ack = next_ack
            hand_check = False

print_info(n_size, n_seg)
deal_with_buffer(buffer)
soc.close()  
