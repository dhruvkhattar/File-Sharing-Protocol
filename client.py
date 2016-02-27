#! /usr/bin/env python

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 7777
s.connect((host,port))
        
s2 = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
host2 = socket.gethostname()
port2 = 7778

print s.recv(1024)

while True:
    n = raw_input()
    s.send(n)
    n2 = n.split()
    rec = s.recv(1024)
    print rec
    rec = rec.split()
    if(n2[0] == 'FileDownload' and n2[1] == 'TCP' and rec[0] != 'Error:'):
        print "start"
        f = s.recv(1024)
        f2 = open(n2[2], 'w')
        f2.write(f)
        f2.close()
        print "end"
    elif(n2[0] == 'FileDownload' and n2[1] == 'UDP'):
        f = s.recvfrom(1024)
        f2 = open(n2[2], 'w')
        f2.write(f)
        f2.close()
s.close()
s2.close()
