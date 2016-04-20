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
        print "Raw message: ",  msg
        print 'Length of received message: %d' % len(msg)
        print "Hex Value: ", ' '.join(hex(ord(n)) for n in msg)
        
        #print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:7]+ ' '+ msg[14:16]+' '+ msg[12:14]+' '+msg[16:19]

        #SIA II & III without text

        if ((msg[2] & '\x3f') == 4) & (len(msg) == 24): #for 4 digit a/c, area 1-9 
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:7]+' '+ msg[12]+ ' '+ msg[13:15]+' '+msg[15:18]
        elif ((msg[2] & '\x3f') == 4) & (len(msg) == 25): #for 4 digit a/c, area 9-64 
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:7]+' '+ msg[12:14]+ ' '+ msg[14:16]+' '+msg[16:19]
        elif ((msg[2] & '\x3f') == 5) & (len(msg) == 25): #for 5 digit a/c, area 1-9 
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:8]+' '+ msg[13]+ ' '+ msg[14:16]+' '+msg[16:19]
        elif ((msg[2] & '\x3f') == 5) & (len(msg) == 26): #for 5 digit a/c, area 9-64 
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:8]+' '+ msg[13:15]+ ' '+ msg[15:17]+' '+msg[17:20]            
        elif ((msg[2] & '\x3f') == 6) & (len(msg) == 26): #for 6 digit a/c, area 1-9 
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:9]+' '+ msg[14]+ ' '+ msg[15:17]+' '+msg[17:20]
        elif ((msg[2] & '\x3f') == 6) & (len(msg) == 27): #for 6 digit a/c, area 9-64
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:9]+' '+ msg[14:16]+ ' '+ msg[16:18]+' '+msg[18:21]

        #SIA II & III with ASCII text

        elif ((msg[2] & '\x3f') == 4) & (len(msg) > 25): #for 4 digit a/c, area 1-9 
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:7]+' '+ msg[12]+ ' '+ msg[13:15]+' '+msg[15:18] + msg[22:-6] #double check the last slicer
        elif ((msg[2] & '\x3f') == 4) & (len(msg) > 26): #for 4 digit a/c, area 9-64 
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:7]+' '+ msg[12:14]+ ' '+ msg[14:16]+' '+msg[16:19]+ msg[23:-6]
        elif ((msg[2] & '\x3f') == 5) & (len(msg) > 26): #for 5 digit a/c, area 1-9 
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:8]+' '+ msg[13]+ ' '+ msg[14:16]+' '+msg[16:19]+ msg[23:-6]
        elif ((msg[2] & '\x3f') == 5) & (len(msg) > 27): #for 5 digit a/c, area 9-64 
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:8]+' '+ msg[13:15]+ ' '+ msg[15:17]+' '+msg[17:20]+ msg[24:-6]         
        elif ((msg[2] & '\x3f') == 6) & (len(msg) > 27): #for 6 digit a/c, area 1-9 
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:9]+' '+ msg[14]+ ' '+ msg[15:17]+' '+msg[17:20]+ msg[24:-6] 
        elif ((msg[2] & '\x3f') == 6) & (len(msg) > 28): #for 6 digit a/c, area 9-64
            print 'SIA '+TimeStamp()+' '+var2+' '+msg[3:9]+' '+ msg[14:16]+ ' '+ msg[16:18]+' '+msg[18:21]+ msg[25:-6] 


            

  

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


