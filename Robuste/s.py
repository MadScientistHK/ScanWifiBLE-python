from util import *
from wif import w
from ble import ble
import threading
import time
import os
#from hcho import gaz

os.system('sudo systemctl start bluetooth')

def Start():
 scanble = threading.Thread(target=ble,args=())
 scanwifi = threading.Thread(target=w,args=())
 sendsaveble = threading.Thread(target=ssb,args=())
 sendsavewifi = threading.Thread(target=ssw,args=())
 mqttlistnerthread = threading.Thread(target=mqttlistner,args=())

 while 1:
     try:
         if mqttlistnerthread.is_alive() == False:
             print 'rerun'
             mqttlistnerthread.start()
     except:error('mqtt broken')
     try:
         if sendsavewifi.is_alive() == False:
             sendsavewifi.start()
     except:error('Can\'t run sendsavewifi thread in s.py')
     try:
         if sendsaveble.is_alive() == False:
             sendsaveble.start()
     except:error('Can\'t run sendsaveble thread in s.py')
     try:
         if scanble.is_alive() == False:
             scanble.start()
     except:error('Can\'t run scanble thread in s.py')
     try:
         if scanwifi.is_alive() == False:
             scanwifi.start()
     except:error('Can\'t run scanWifi thread in s.py')

Start()


