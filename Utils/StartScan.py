import threading
import time
import os
import sys
import wifi
import base64
import csv
import json

os.system('sudo systemctl start bluetooth')
if os.path.isdir("/home/pi/Data") != True:
    os.system("sudo mkdir /home/pi/Data")
try:
    if os.path.isdir("/media/usb/Data") != True:
    	os.system("sudo mkdir /media/usb/Data")
except:error("usb stick unmounted")

time.sleep(5)
#####################################################################################################
###########################_CHECK_THE_INTERNET_CONNECTION_###########################################
#####################################################################################################

def checkInternet():
    return False

#####################################################################################################
###########################_SEARCH_IF_THERE_IS_NUMBER_IN_A_STRING_###################################
#####################################################################################################

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

#####################################################################################################
###########################_RETURN_THE_NUMBER_MAX_OF_NAME_FILE_######################################
#####################################################################################################

def error(msg):
    a=0
    print msg
    #log = open('logError.txt','a')
    #log.write('\n Error at : '+str(time.time())+' , '+str(msg))
    #log.close()

#####################################################################################################
###########################_CONVERTS_WIFI.CSV_FILE_TO_JSON_##########################################     
#####################################################################################################

def wcj(file):
    try:
	try:
	    csvfile = open(file, 'r')
    	except:error('Can\'t convert in csv to json the file :'+str(file)+' (wifi) in wcj(util.py)' )
    	try:
	    jfile = file[:-3]+"json"
    	    jsonfile = open(jfile, 'w')
    	except:error('Can\'t create json in wcj(util.py)')
    	try:
    	    reader = csv.DictReader(csvfile,("ID","TimeStamp","b64","BSSID","channel","RSSI","EncryptionKey","SSID","Chiffrement","idp"))
    	    out = json.dumps( [ row for row in reader ] )
    	    jsonfile.write(out)
	    os.system('sudo rm '+file)
	    return jfile
    	except:error('Can\'t write json in wcj(util.py)')
    except:error('Can\'t convert (wifi) csv to json in wcj(util.py)')

#####################################################################################################
###########################_GET_THE_SERIALNUMBER_####################################################     
#####################################################################################################

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial

#####################################################################################################
#####################################################################################################
#####################################################################################################

def SearchW(comp):
	
    #Scan every wifi around
    try:
        cells = wifi.Cell.all('wlan0')
    except:error('wlan0 busy, can\'t scan (wif.py)')
    
    #If the program restart, there might be some old files, to avoid to lost them by rewrite, we skip it for the name, and send it later
    try:
    	while os.path.isfile('/home/pi/Data/wifi_'+str(comp)+'.json') == True or os.path.isfile('/home/pi/Data/sw_'+str(comp)+'.json') == True:
	    comp=comp+1
    except:error('Failed to skip the name (wif.py)')
    
    #Changing name in case we lost connection
    try:
    	if checkInternet() == True:
	    file = '/home/pi/Data/wifi_'+str(comp)+'.csv'
	    idp = "wifi_"+str(comp)
    	else:
	    file = '/home/pi/Data/sw_'+str(comp)+'.csv'
	    idp = "sw_"+str(comp)
    	id = str(getserial())+','
    	b64 = 'true,'
    except:error('Failed to write the name of the file (wif.py)')
    
    #Create file to send data
    try:
	print file
     	f = open(file,'w')
    except:error('Failed to create file for scan (wif.py)')
    
    #Get data of scanning, all the data is in base64 to avoid error about special character
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
	os.system("sudo cp "+jfile+" /media/usb/Data")
    except:error("usb stick unmounted")

#If it miss a message, it look back to resend missing file
def lookBackW(comp):
    if comp == 0:
	i=0
    else:
	i=1
    for i in range(comp):
	time.sleep(1)
        if os.path.isfile('/home/pi/Data/wifi_'+str(comp-i)+'.json')== True:
            send('/home/pi/Data/wifi_'+str(comp-i)+'.json')
	    print 'i found a lost lamb'

#Scan wifi every 10 seconds
def w():
    comp = 0
    while 1:
        print "\n=========================== Scan Wifi Start =========================\n"
	try:
            SearchW(comp)
            comp=comp+1
            print comp
        except:error('\n Error at : '+str(time.time())+' . Can\'t run scanWifi in sw.py')
        print "\n========================= Scan Wifi Complete ========================\n"
        time.sleep(10)

w()


