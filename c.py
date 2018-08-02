import os
import time
import threading

cmd = "sudo iw dev wlan0 station dump | awk '($1 ~ /Station$/) {s = $2;print s;}' >> num.txt"


def clock():
    on='ifconfig wlan0 up'
    off='ifconfig wlan0 down'
    while 1:
	os.system(off)
    	os.system(on)
	time.sleep(60)

def ap2():
    free_sfr = True
    while 1:
        if free_sfr == True:
            os.system('sudo create_ap -n wlan0 FreeWifi')
            free_sfr = False
        else:
            os.system('sudo create_ap -n wlan0 SfrWifi')
            free_sfr = True

def ap():
    os.system('sudo create_ap -n wlan0 orange')


ct = threading.Thread(target=clock,args=())
#ct.start()

t = threading.Thread(target=ap,args=())
t.start()


while 1:
    i=0
    timestamp = time.time()
    date = time.ctime()
    os.system(cmd)
    count = 0
    g = open('address.txt','r')
    f = open('num.txt','r')
    add = g.readlines()
    num = f.readlines()
    print num
    append = True
    for mac in num:
        timestamp = time.time()
        if len(add) == 0:
            g.close()
            g=open('address.txt','w')
            g.write(mac[:-1]+','+str(timestamp)+','+str(date)+'\n')
            g.close()
        else:
            g.close()
            g=open('address.txt','a')
            g.write(mac[:-1]+','+str(timestamp)+','+str(date)+'\n')
            g.close()
            #for i in range(len(add)):
              #  if mac == add[i]:
             #       append = False
            #if append == True:
                #g.close()
                #g=open('address.txt','a')
                #g.write(str(mac)+','+str(timestamp))
                #g.close()
    f.close()
    os.system('sudo rm num.txt')
    g=open('address.txt','r')
    count = g.readlines()
    print len(count)
    time.sleep(5)
