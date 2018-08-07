

import blescan
import sys
import threading
import os
import bluetooth._bluetooth as bluez
import time
from util import *

#Start bluetooth interface
os.system('sudo systemctl start bluetooth')

#Scan BLE function, with 1 parameter to count each time it scans
def scanble(comp):
	
    #Initialize bluetooth interface
    dev_id = 0
    try:
    	sock = bluez.hci_open_dev(dev_id)
    except:
	error("error accessing bluetooth device... in ble.py")
    	sys.exit(1)
	
    #Get the serial number of the raspberry to get a unique id
    id = getserial()
	
    #While there is file named "ble_x.json" or "sb_x.json" add +1 to the comp var, to avoid rewritting file or try to send nothing
    while os.path.isfile('ble_'+str(comp)+'.json') == True or os.path.isfile('sb_'+str(comp)+'.json') == True:
        comp=comp+1
	
    #When there is internet connection, it names the new file as "ble_x.csv" and "sb_x.csv" when there is no connection 
    #Idp identify the packet
    if checkInternet() == True:
	file = 'ble_'+str(comp)+'.csv'
	idp = 'ble_'+str(comp)
    else:
	file = 'sb_'+str(comp)+'.csv'
        idp = 'sb_'+str(comp)
    
    #Open a new file with the right name as above
    f = open(file,'w')

    #Used to get the time spent to send the file
    t1 = time.time()

    #Start the event for the scan
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    
    savebeacon = []

    #Return 50 ble scanned
    returnedList = blescan.parse_events(sock,50)
    
    #Second var to get the time spent to send
    t2 = time.time()
    
    #Print how many second it spent to send
    print "scan ble : "+str(t2-t1)
    finalList = []
    
    #Check if a scanned ble is already in the finalList
    for beacon in returnedList:
        if str(beacon[0:17]) not in str(finalList):
	    finalList.append(str(beacon))
	    savebeacon = finalList
		
    #Write the results in the csv file
    for beacon in finalList:
            stamp = time.time()
    	    beacon = beacon.replace("\"","")
            f.write(str(id)+","+str(stamp)+","+beacon+","+idp+"\n")
    f.close()

    #Reopen the file in read mode
    f = open(file,'r')

    #Convert csv to json
    jfile = bcj(file)

    #If there is still internet, send the json file and look back if there is no file that hasn't been sent yet
    if checkInternet() == True:
	send(jfile)
	lookBack(comp)

#Look back if there is no file that hasn't been sent yet
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

#Scan every 10 seconds
def ble():
    comp=0
    while 1:
        print '\n=========================== Scan BLE Start ==========================\n'
        try:
	    scanble(comp)
	    comp=comp+1
            print comp
	except:error('Error at : '+str(time.time())+' . Can\'t run scanble in ble.py')
        print '\n========================= Scan BLE Complete =========================\n'
        time.sleep(10)




