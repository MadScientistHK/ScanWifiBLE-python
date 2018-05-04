
import csv
import blescan
import sys
import threading
import os
import bluetooth._bluetooth as bluez
import time 
from uuid import getnode as get_mac
from blecsvjson import bcj
from send import send
from checkInternet import checkInternet

os.system('sudo systemctl start bluetooth')



def scanble():
    dev_id = 0
    try:
    	sock = bluez.hci_open_dev(dev_id)

    except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    stop = 0
    savebeacon = []
    c = open("scanble.csv", "w")
    while stop != 1:
	returnedList = blescan.parse_events(sock,30)
	finalList = []
	for beacon in returnedList:
	    if str(beacon[0:17]) not in str(finalList):
		finalList.append(str(beacon))
	    else: pass
	savebeacon = finalList
	for beacon in finalList:
            stamp = time.time()
	    beacon = beacon.replace("\"","")
	    macID = get_mac()
	    c.write(str(macID)+","+str(stamp)+","+beacon+"\n")
	stop = stop + 1
	c.close()
    bcj('scanble.csv')
    o=0
    if checkInternet() == True :
       try:
           send('scanble.json')
       except:
           print 'error while sending'
    else : 
	while os.path.isfile('saveble'+str(o)+'.csv')==True:
	    o=o+1
	saveble = open('saveble'+str(o)+'.csv','a')
	for beacon in savebeacon:
	    stamp = time.time()
	    fichtre = get_mac()
	    saveble.write(str(fichtre)+","+str(stamp)+","+beacon+"\n")
	saveble.close()


def ble():
    os.system('sudo systemctl start bluetooth')
    while 1:
        print '\n=========================== Scan BLE Start ==========================\n'
        scanble()
        print '\n========================= Scan BLE Complete =========================\n'
        time.sleep(10)


