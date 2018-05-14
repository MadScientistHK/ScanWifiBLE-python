
from sw import wifi
from ble import ble
import threading
import time
import os
from blecsvjson import bcj
from wificsvjson import wcj
from send import send
from checkInternet import checkInternet
os.system('sudo systemctl start bluetooth')

def ssb():
    while 1:
       # print 'Thread sendsaveble start'
        o=0
        while o < len(os.listdir('/home/pi')):
            if os.path.isfile('saveble'+str(o)+'.csv')==True and os.path.getsize('/home/pi/saveble'+str(o)+'.csv') > 0 :
                saveble = open('saveble'+str(o)+'.csv','r')
                if saveble.readlines != []:
		    print 'i was there'
                    try:
			if checkInternet() == True:
		           bcj('saveble'+str(o)+'.csv')
                           send('saveble'+str(o)+'.json')
                           saveble.close()
                           print 'saveble'+str(o)+' has been send'
                           if os.path.isfile('saveble'+str(o)+'.csv')==True:
                               os.system('sudo rm saveble'+str(o)+'.csv')
		           else:
			       print 'not delete or not found'
                    except:
                        print 'error while sending'
	    else:
		if os.path.isfile('saveble'+str(o)+'.csv')==True:
		    os.system('sudo rm saveble'+str(0)+'.csv')
	    if os.path.isfile('saveble'+str(o)+'.json')==True:
                os.system('sudo rm saveble'+str(o)+'.json')
	        print 'json delete'
	    o=o+1


def ssw():
    while 1:
       # print 'Thread sendsavewifi start'
        o=0
        while o < len(os.listdir('/home/pi')):
            if os.path.isfile('savewifi'+str(o)+'.csv')==True and os.path.getsize('/home/pi/savewifi'+str(o)+'.csv') > 0:
                savewifi = open('savewifi'+str(o)+'.csv','r')
                if savewifi.readlines != []:
                    print 'Je suis passe par la'
                    try:
		        if checkInternet() == True:
                            wcj('savewifi'+str(o)+'.csv')
                            send('savewifi'+str(o)+'.json')
                            savewifi.close()
                            print '\nSavewifi'+str(o)+' has been send \n'
                            if os.path.isfile('savewifi'+str(o)+'.csv')==True:
                                os.system('sudo rm savewifi'+str(o)+'.csv')
                            else:
                                print 'not delete or not found'
			else:print "OMG CA MARCHE PAS"
                    except:
                        print 'error while sending'
	    else:
                if os.path.isfile('savewifi'+str(o)+'.csv')==True:
                    os.system('sudo rm savewifi'+str(o)+'.csv')
            if os.path.isfile('savewifi'+str(o)+'.json')==True:
                os.system('sudo rm savewifi'+str(o)+'.json')
                print 'json delete'
            o=o+1

def Start():
 scanble = threading.Thread(target=ble,args=())
 scanwifi = threading.Thread(target=wifi,args=()) 
 sendsaveble = threading.Thread(target=ssb,args=())
 sendsavewifi = threading.Thread(target=ssw,args=())

 sendsavewifi.start()
 sendsaveble.start()
 scanble.start()
 scanwifi.start()

Start()

