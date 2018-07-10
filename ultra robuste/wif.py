import wifi
import threading
import time
import os
import base64
from util import *

def Search(comp):
    #Scan every wifi around
    try:
        cells = wifi.Cell.all('wlan0')
    except:error('wlan0 busy, can\'t scan (wif.py)')
    #If the program restart, there might be some old files, to avoid to lost them by rewrite, we skip it for the name, and send it later
    try:
    	while os.path.isfile('wifi_'+str(comp)+'.json') == True or os.path.isfile('sw_'+str(comp)+'.json') == True:
	    comp=comp+1
    except:error('Failed to skip the name (wif.py)')
    #Changing name in case we lost connection
    try:
    	if checkInternet() == True:
	    file = 'wifi_'+str(comp)+'.csv'
	    idp = "wifi_"+str(comp)
    	else:
	    file = 'sw_'+str(comp)+'.csv'
	    idp = "sw_"+str(comp)
    	id = str(getserial())+','
    	b64 = 'true,'
    except:error('Failed to write the name of the file (wif.py)')
    #Create file to send data
    try:
     	f = open(file,'w')
    except:error('Failed to create file for scan (wif.py)')
    #Get data of scaning, all the data is in base64 to avoid error about special character
    try:
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
	    #Writing data
	    try:
      		f.write(row)
	    except:error('Failed to write the file (wif.py)')
    except:error('Failed to collect data (wif.py)')
    #Close and open the file to save the data before conversion
    try:
        f.close
        f = open(file,'r')
    except:error('Failed to open the file (wif.py)')
    #Convert csv to json
    try:
        jfile = wcj(file)
    except:error('Failed to convert the file (wif.py)')
    #Sending the file if there is a internet connection
    try:
	if checkInternet() == True:
    	    send(jfile)
	    try:
		lookBack(comp) #If we miss a message, we look back to resend missing file
    	    except:error('Failed to send missing file (wif.py)')
    except:error('Failed to send the file (wif.py)')

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
        except:error('\n Error at : '+str(time.time())+' . Can\'t run scanWifi in sw.py')
        print "\n========================= Scan Wifi Complete ========================\n"
        time.sleep(10)

