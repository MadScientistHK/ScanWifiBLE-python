import wifi
import threading
import time
import os
import base64
from util import *

def Search(comp):
    cells = wifi.Cell.all('wlan0')
    while os.path.isfile('wifi_'+str(comp)+'.json') == True or os.path.isfile('sw_'+str(comp)+'.json') == True:
	comp=comp+1
    lb = threading.Thread(target=lookBack,args=(comp,))
    if checkInternet() == True:
	file = 'wifi_'+str(comp)+'.csv'
	idp = "wifi_"+str(comp)
    else:
	file = 'sw_'+str(comp)+'.csv'
	idp = "sw_"+str(comp)
    f = open(file,'w')
    id = str(getserial())+','
    b64 = 'true,'
    for cell in cells:
	timestamp = base64.b64encode(str(time.time()))+','
	bssid = base64.b64encode(str(cell.address))+','
	channel = base64.b64encode(str(cell.channel))+','
	rssi = base64.b64encode(str(cell.signal))+','
	encryption = base64.b64encode(str(cell.encrypted))+','
	ssid = base64.b64encode(str(cell.ssid))+','
	if encryption == base64.b64encode('True')+',': chiffrement = base64.b64encode(str(cell.encryption_type))+','
	else: chiffrement = base64.b64encode('Not protected')+','
	row = id+timestamp+b64+bssid+channel+rssi+encryption+ssid+chiffrement+idp+'\n'
	f.write(row)
    f.close
    f = open(file,'r')
    jfile = wcj(file)
    if checkInternet() == True:
    	send(jfile)
#	lb.start()
	lookBack(comp)


def lookBack(comp):
    if comp == 0:
	i=0
    else:
	i=1
    for i in range(comp):
	time.sleep(1)
        if os.path.isfile('wifi_'+str(comp-i)+'.json')== True:
            send('wifi_'+str(comp-i)+'.json')
	    print 'i found a lost lamb'


def w():
    comp = 0
    while 1:
        print "\n=========================== Scan Wifi Start =========================\n"
	try:
            Search(comp)
            comp=comp+1
            print comp
        except:
            log = open('logError.txt','a')
            log.write('\n Error at : '+str(time.time())+' . Can\'t run scanWifi in sw.py')
            log.close()
        print "\n========================= Scan Wifi Complete ========================\n"
        time.sleep(10)

