#! /usr/bin/env python

import datetime
import time
import os
import subprocess
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 7777
s.bind((host,port))

s.listen(5)
                
s2 = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
host2 = socket.gethostname()
port2 = 7778
s2.bind(("",port2))
                
while True:
    
    c, addr = s.accept()
    print 'Got connection from', addr
    c.send('Connection successful')
    
    while True:

        var = c.recv(1024)
        var2 = var.split()
        if len(var2) == 0:
            break
        elif var2[0] == "IndexGet":
            if len(var2) == 1:
                c.send('\nError: No flag given as input.\n')
            elif len(var2) != 4 and var2[1] == 'shortlist':
                c.send('\nError: Enter the StartTime and the EndTime.\n')
            elif var2[1] == 'longlist' or var2[1] == 'shortlist':
                output = subprocess.check_output('ls', shell=True)
                fnames = output.split()
                details = '\n'
                if len(var2) == 4:
                    start = time.strptime(var2[2], "%d/%m/%Y")
                    end = time.strptime(var2[3], "%d/%m/%Y")
                for fname in fnames:
                    tp = subprocess.check_output('file ' + fname, shell=True)
                    tp = tp.split("\n")
                    new = str(tp[0])
                    sz = os.path.getsize(fname)
                    new = new + " " + str(sz)
                    t = os.path.getmtime(fname)
                    tim = time.strftime("%d/%m/%Y",time.gmtime(t))
                    ti = time.strptime(tim, "%d/%m/%Y")
                    new = new + " " + str(tim) + "\n"
                    if var2[1] == 'shortlist':
                        if ti >= start and ti <= end:
                            details = details + new
                    else:
                        details = details + new
                c.send(details)
        elif var2[0] == "FileHash":
            if len(var2) == 1:
                c.send('\nError: Wrong flag or no flag given as input\n')
            elif var2[1] == "verify":
                if len(var2) == 2:
                    c.send('\nError: File name not given.\n')
                else:
                    com = 'md5sum'+' '+var2[2]+' | '+'awk \'{print $1}\''
                    try:
                        time123 = str(datetime.datetime.fromtimestamp(os.path.getmtime(var2[2])))
                        temp = subprocess.check_output(com, shell = True).split("\n")
                        output = '\n' + temp[0]+' '+time123 + '\n'
                        c.send(output)
                    except:
                        c.send('\nError: No such File Present.\n')
            elif var2[1] == "checkall":
                files = subprocess.check_output('find . -type f', shell=True)
                files_list = files.split()
                final = '\n'
                for f in files_list:
                    com = 'md5sum'+' '+f+' | '+'awk \'{print $1}\''
                    time123 = str(datetime.datetime.fromtimestamp(os.path.getmtime(f)))
                    temp = subprocess.check_output(com, shell = True).split("\n")
                    output = f+' '+temp[0]+' '+time123
                    final = final+output+'\n'
                c.send(final)
        elif var2[0] == 'FileDownload':
            if var2[1] == "TCP":
                if len(var2) == 2:
                    c.send('\nError: no filename specified\n')
                else:
                    try:
                        com = 'md5sum'+' '+var2[2]+' | '+'awk \'{print $1}\''
                        time123 = str(datetime.datetime.fromtimestamp(os.path.getmtime(var2[2])))
                        temp = subprocess.check_output(com, shell = True).split("\n")
                        sz = os.path.getsize(var2[2])
                        output = '\n' +var2[2]+' '+str(sz)+' '+ temp[0]+' '+ time123 + '\n'
                        print 'sending hash'
                        c.send(output)
                        print 'done'
                        f = open(var2[2], 'r')
                        c.send(f.read())
                        f.close()
                    except:
                        c.send('\nError: Filename specified does not exist.\n')

            elif var2[1] == "UDP":
                if len(var2) == 2:
                    s2.sendto('Error: No filename specified',(host2,port2))
                else:
                    com = 'md5sum'+' '+var2[2]+' | '+'awk \'{print $1}\''
                    time123 = str(datetime.datetime.fromtimestamp(os.path.getmtime(var2[2])))
                    temp = subprocess.check_output(com, shell = True).split("\n")
                    sz = os.path.getsize(var2[2])
                    output = '\n' +var2[2]+' '+str(sz)+' '+ temp[0]+' '+ time123 + '\n'
                    s2.sendto(output,(host2,port2))
                    f = open(var2[2], 'r')
                    s2.sendto(f.read(),(host2,port2))
                    f.close()
            else:
                c.send('\nError: Wrong flag or no flag given as input\n')
        else:
            c.send('Error : Wrong Command')
    c.close()
s.close()
s2.close()
