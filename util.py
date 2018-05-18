import socket
import csv
import json
import sys
import threading
import time
import os


def checkInternet():
    connected = False
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("www.google.com", 80))
        connected = True
        return connected
    except socket.gaierror, e:
        print "Not connected"
    return connected

def error(msg):
    log = open('logError.txt','a')
    log.write('\n Error at : '+str(time.time())+' , '+str(msg))
    log.close()


def ssw():
    try:
    	while 1:
            i=0
            list = os.listdir('/home/pi')
            while 'b' in list[0]:
		try:
            	    if os.path.isfile('savewifi'+str(i)+'.csv')==True and os.path.getsize('/home/pi/savewifi'+str(i)+'.csv') > 0:
			savewifi = open('savewifi'+str(i)+'.csv','r')
                        if savewifi.readlines != []:
                            try:
                                if checkInternet() == True:
                            	    wcj('savewifi'+str(i)+'.csv')
                            	    send('savewifi'+str(i)+'.json')
                            	    savewifi.close()
                            	    print '\nSavewifi'+str(i)+' has been send \n'
                            except:error('Can\t run wcj or send function in ssw(util.py) ')
                    elif os.path.isfile('savewifi'+str(i)+'.csv')==True:
                        os.system('sudo rm savewifi'+str(i)+'.csv')
                    elif os.path.isfile('savewifi'+str(i)+'.json')==True:
                        os.system('sudo rm savewifi'+str(i)+'.json')
                        print 'json delete'
		except:error('Can\'t remove old file')
                i=i+1
    except:error('Can\'t send savewifi in ssw(util.py)')

def ssb():
    try:
        while 1:
            i=0
            list = os.listdir('/home/pi')
            while 'b' in list[0] :
                try:
                    if os.path.isfile('saveble'+str(i)+'.csv')==True and os.path.getsize('/home/pi/saveble'+str(i)+'.csv') > 0:
                        saveble = open('saveble'+str(i)+'.csv','r')
                        if saveble.readlines != []:
                            try:
                                if checkInternet() == True:
                                    wcj('saveble'+str(i)+'.csv')
                                    send('saveble'+str(i)+'.json')
                                    saveble.close()
                                    print '\nSaveble'+str(i)+' has been send \n'
                            except:error('Can\t run wcj or send function in ssw(util.py) ')
                    elif os.path.isfile('saveble'+str(i)+'.csv')==True:
                        os.system('sudo rm saveble'+str(i)+'.csv')
                    elif os.path.isfile('saveble'+str(i)+'.json')==True:
                        os.system('sudo rm saveble'+str(i)+'.json')
                        print 'json delete'
		except:error('Can\'t remove old file')
                i=i+1
    except:error('Can\'t send saveble in ssw(util.py)')


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
        cmd = "sudo curl -H \"Content-Type: application/json; charset=UTF-8\" -X POST -k -d \"{\\\"toInsert\\\":"+str(txt[0])+"}\" https://c-cada2.mybluemix.net/InsertManyData"
        os.system(str(cmd))
    except:
        error('No internet connection')
        print 'No connection'

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
    	    reader = csv.DictReader(csvfile,("ID","TimeStamp","BSSID","frequency","Channel","RSSI","EncryptionKey","SSID","Chiffrement","idp"))
    	    out = json.dumps( [ row for row in reader ] )
    	    jsonfile.write(out)
    	except:error('Can\'t write json in wcj(util.py)')
    except:error('Can\'t convert (wifi) csv to json in wcj(util.py)')

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


