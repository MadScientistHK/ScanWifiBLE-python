import os
import time
import threading

cmd = "sudo iw dev wlan0 station dump | awk '($1 ~ /Station$/) {s = $2;print s;}' >> num.txt"

def ap():
    os.system('sudo create_ap -n wlan0 FreeWifi')
    
t = threading.Thread(target=ap,args=())
t.start()

while 1:
    i=0
    timestamp = time.time()
    os.system(cmd)
    count = 0
    g = open('address.txt','r')
    f = open('num.txt','r')
    add = g.readlines()
    num = f.readlines()
    print num
    append = True
    for mac in num:
        if len(add) == 0:
            g.close()
            g=open('address.txt','w')
            g.write(str(mac))
            g.close()
        else:
            for i in range(len(add)):
                if mac == add[i]:
                    append = False
            if append == True:
                g.close()
                g=open('address.txt','a')
                g.write(str(mac))
                g.close()
    f.close()
    os.system('sudo rm num.txt')
    g=open('address.txt','r')
    count = g.readlines()
    print len(count)
    time.sleep(5)