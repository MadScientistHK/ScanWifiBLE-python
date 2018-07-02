
import socket
import csv
import json
import sys
import threading
import time
import os

#####################################################################################################
###########################_CHECK_THE_INTERNET_CONNECTION_###########################################
#####################################################################################################

def checkInternet():
    connected = False
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("Awww.google.com", 80))
        connected = True
        return connected
    except socket.gaierror, e:
        print "Not connected"
    return connected

#####################################################################################################
###########################_WRITE_LOG_IF_ERROR_######################################################
#####################################################################################################

def error(msg):
    log = open('logError.txt','a')
    log.write('\n Error at : '+str(time.time())+' , '+str(msg))
    log.close()

#####################################################################################################
###########################_SEND_THE_SAVES_OF_THE_WIFI_SCAN_#########################################     
#####################################################################################################

def ssw():
    try:
    	while 1:
            i=0
            list = os.listdir('/home/pi')
            while '.' in list[0]:
		try:
            	    if os.path.isfile('savewifi'+str(i)+'.csv')==True and os.path.getsize('/home/pi/savewifi'+str(i)+'.csv') > 0:
			savewifi = open('savewifi'+str(i)+'.csv','r')
                        if savewifi.readlines != []:
                            try:
                                if checkInternet() == True:
                            	    wcj('savewifi'+str(i)+'.csv')
                            	    send('savewifi'+str(i)+'.json')
                            	    savewifi.close()
				    os.system('sudo rm savewifi'+str(i)+'.csv')
                            	    print '\nSavewifi'+str(i)+' has been send \n'
                            except:error('Can\t run wcj or send function in ssw(util.py) ')
                    elif os.path.isfile('savewifi'+str(i)+'.csv')==True:
                        os.system('sudo rm savewifi'+str(i)+'.csv')
                    if os.path.isfile('savewifi'+str(i)+'.json')==True:
                        os.system('sudo rm savewifi'+str(i)+'.json')
                        print 'json delete'
		except:error('Can\'t remove old file in ssw(util.py)')
                i=i+1
    except:error('Can\'t send savewifi in ssw(util.py)')

#####################################################################################################
###########################_SEND_THE_SAVES_OF_THE_BLE_SCAN_##########################################     
#####################################################################################################

def ssb():
    try:
        while 1:
            i=0
            list = os.listdir('/home/pi')
            while '.' in list[0] :
                try:
                    if os.path.isfile('saveble'+str(i)+'.csv')==True and os.path.getsize('/home/pi/saveble'+str(i)+'.csv') > 0:
                        saveble = open('saveble'+str(i)+'.csv','r')
                        if saveble.readlines != []:
                            try:
                                if checkInternet() == True:
                                    bcj('saveble'+str(i)+'.csv')
                                    send('saveble'+str(i)+'.json')
                                    saveble.close()
				    os.system('sudo rm saveble'+str(i)+'.csv')
                                    print '\nSaveble'+str(i)+' has been send \n'
                            except:error('Can\t run wcj or send function in ssb(util.py) ')
                    elif os.path.isfile('saveble'+str(i)+'.csv')==True:
                        os.system('sudo rm saveble'+str(i)+'.csv')
                    if os.path.isfile('saveble'+str(i)+'.json')==True:
                        os.system('sudo rm saveble'+str(i)+'.json')
                        print 'json delete'
		except:error('Can\'t remove old file in ssb(util.py)')
                i=i+1
    except:error('Can\'t send saveble in ssb(util.py)')

#####################################################################################################
###########################_THE_SEND_FUNCTION__######################################################     
#####################################################################################################

def send(file):
    try:
        data = open(file,'r')
        txt = data.readlines()
    	if txt == []:
            os.system('sudo rm '+str(file))
    	else:
            txt[0] = txt[0].replace("\"","\\\"")
    except:error('Can\'t send at send(util.py), can\'t open the file :'+str(file))
    try:
	t1 = time.time()
	udp(str(txt[0]),5100,'81.250.16.95')
        #t1 = time.time()
        #cmd = "sudo curl -H \"Content-Type: application/json; charset=UTF-8\" -X POST -k -d \"{\\\"toInsert\\\":"+str(txt[0])+"}\" https://c-cada2.mybluemix.net/Positionb64"
        #os.system(str(cmd))
	t2 = time.time()
	print t2-t1
    except:
        error('No internet connection')
        print 'No connection'

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
    	    reader = csv.DictReader(csvfile,("ID","TimeStamp","b64","BSSID","frequency","RSSI","EncryptionKey","SSID","Chiffrement","idp"))
    	    out = json.dumps( [ row for row in reader ] )
    	    jsonfile.write(out)
    	except:error('Can\'t write json in wcj(util.py)')
    except:error('Can\'t convert (wifi) csv to json in wcj(util.py)')

#####################################################################################################
###########################_CONVERTS_BLE.CSV_FILE_TO_JSON_###########################################     
#####################################################################################################

def bcj(file):
    try:
	try:
            csvfile = open(file, 'r')
    	except:error('Can\'t open the file :'+str(file)+' (ble) in bcj(util.py)' )
    	try:
	    jfile = file[:-3]+"json"
    	    jsonfile = open(jfile, 'w')
    	except:error('Can\'t create json in bcj(util.py)')
    	try:
	    fieldnames = ("ID","TimeStamp","MAC","UDID","Minor","Major","TX","RSSI","idp")
    	    reader = csv.DictReader(csvfile,fieldnames)
    	    out = json.dumps( [ row for row in reader ] )
    	    jsonfile.write(out)
    	except:error('Can\'t write json in bcj(util.py)')
    except:error('Can\'t convert (ble) csv to json in bcj(util.py)')

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
###########################_UDP_SENDER_FUNCTION_#####################################################     
#####################################################################################################

def udp(data, port=5100, addr='81.250.16.95'):
    #t1 = time.time()
    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Make the socket multicast-aware, and set TTL.
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
    # Send the data
    s.sendto(data, (addr, port))
    #t2 = time.time()
    #print t2-t1
