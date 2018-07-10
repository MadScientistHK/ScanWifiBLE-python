

import blescan
import sys
import threading
import os
import bluetooth._bluetooth as bluez
import time
from util import *

os.system('sudo systemctl start bluetooth')

def scanble(comp):
    dev_id = 0
    id = getserial()
    try:
    	sock = bluez.hci_open_dev(dev_id)

    except:
	error("error accessing bluetooth device... in ble.py")
    	sys.exit(1)

    while os.path.isfile('ble_'+str(comp)+'.json') == True or os.path.isfile('sb_'+str(comp)+'.json') == True:
        comp=comp+1

    if checkInternet() == True:
	file = 'ble_'+str(comp)+'.csv'
	idp = 'ble_'+str(comp)
    else:
	file = 'sb_'+str(comp)+'.csv'
        idp = 'sb_'+str(comp)


    f = open(file,'w')
    t1 = time.time()
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    stop = 0
    savebeacon = []
    while stop != 1:
	returnedList = blescan.parse_events(sock,30)
	t2 = time.time()
	print "scan ble : "+str(t2-t1)
	finalList = []
	for beacon in returnedList:
	    if str(beacon[0:17]) not in str(finalList):
		finalList.append(str(beacon))
	savebeacon = finalList
	for beacon in finalList:
            stamp = time.time()
	    beacon = beacon.replace("\"","")
	    f.write(str(id)+","+str(stamp)+","+beacon+","+idp+"\n")
	stop = stop + 1
    f.close()
    f = open(file,'r')
    jfile = bcj(file)
    if checkInternet() == True:
	send(jfile)
	lookBack(comp)

def lookBack(comp):
    if comp == 0:
        i=0
    else:
        i=1
    for i in range(comp):
        time.sleep(1)
        if os.path.isfile('ble_'+str(comp-i)+'.json')== True:
            send('ble_'+str(comp-i)+'.json')
	    print 'i found a lost lamb'

def ble():
    os.system('sudo systemctl start bluetooth')
    comp=0
    while 1:
        print '\n=========================== Scan BLE Start ==========================\n'
        try:
	    scanble(comp)
	    comp=comp+1
            print comp
	except:
    	    log = open('logError.txt','a')
    	    log.write('\n Error at : '+str(time.time())+' . Can\'t run scanble in ble.py')
    	    log.close()
        print '\n========================= Scan BLE Complete =========================\n'
        time.sleep(10)



