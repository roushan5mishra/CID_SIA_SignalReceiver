# Scipt Name: arc.py

# Author: Roushan Mishra (roushan5mishra@gmail.com)

# Version: 1.0
# Created: 16-Apr-16

# Description: This script reads the data received on localhost, port 10006 and decodes it from Contact Id or SIA Level II format

import socket
import re
import time
import datetime

def TimeStamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    return st

def ContactID(msg):
    if len(msg) < 13:
        print "invalid data received\n"
        
    else:
        #print "Raw message: ", msg
        print 'CID '+TimeStamp()+' '+var2+' '+ msg[1:5] +(' E 'if msg[7]== 1 else ' R ')+msg[8:11]+' '+msg[11:13]+' '+msg[13:16]

def SIA(msg):
    if len(msg) < 13:
        print "invalid data received\n"
        
    else:
        #print "Raw message: ",  msg
        #print "Raw message: ", ' '.join(hex(ord(n)) for n in msg)
        #print len(msg)
        print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:7]+ ' '+ msg[14:16]+' '+ msg[12:14]+' '+msg[16:19]
  

def DecodeData(data):

    events = [
        [r'2[\x00-\xff]{,}$'], 'contactID', ContactID,
        [r'3[\x00-\xff]{,}$'], 'SIA', SIA
        ]

    for index in range(0, len(events), 3):
        obj = re.match(''.join(events[index]), data)
        if obj is not None:
            #print events[index+1] + ' Message received...\n'
            a = events[index+2]
            a(data)
            break
    #return 0

def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname() # get local machine name
    port = 10006
    s.bind((host, port))  #Binding the port with host
    global var2 

    while True:   

        try:

            s.listen(5)        
            c, addr = s.accept() #Establishing connection with the client.
            print 'Got connection from', addr
            
            var1 = str(addr)
            var2 = str(var1[2:14]+ var1[16:-1])

            while True:
                data = c.recv(1024)
                if not data:
                    break
                if len(data) < 13:
                    continue

                #print data   
                #print 'a/c: '+data[1:5]+' E(1)/R(0): '+data[7]+' Event Code: '+data[8:11]+' area: '+data[11:13]+' zone/user: '+data[13:]
                #print 'interpreting message.....'
                DecodeData(data)

                text = '\x06\x0D\x0A'

                c.send(text)
                #print 'ack sent'
            c.close()
        
        except socket.error:
            break

if __name__ == '__main__':
    main()


