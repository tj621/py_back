# coding=utf-8
'''

@author: Zxh
'''
# import serial
from time import sleep
import binascii
import threading

a = 1
# try:
# serialport = serial.Serial("/dev/ttyAMA0",9600,timeout=1)
# except:
#     print 'serial error: there is no COM or COM was occupied'

mutex = threading.Lock()


def send_command(data):
    global mutex, a
    data = bytes(bytearray.fromhex(data))
    if mutex.acquire():
        #         sleep(2)
        #         serialport.write(data)
        #         while serialport.inWaiting()>0:
        #             pass
        print 'output correct  ' + str(a)
        #         recv=serialport.readline()
        #         recv=binascii.b2a_hex(recv)
        a = a + 1
        #         print 'output correct  '+str(a)
        mutex.release()


# 	sleep(0.03)
#     return recv

def query_all_state(Query):
    recv = send_command(Query)
    return recv
    
