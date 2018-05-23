from util import *
from sw import wifi
from ble import ble
import threading
import time
import os
from hcho import gaz

os.system('sudo systemctl start bluetooth')

def Start():
 scanble = threading.Thread(target=ble,args=())
 scanwifi = threading.Thread(target=wifi,args=()) 
 sendsaveble = threading.Thread(target=ssb,args=())
 sendsavewifi = threading.Thread(target=ssw,args=())
# threadgaz = threading.Thread(target=gaz,args=())
# threadgaz.start()
 try:
  sendsavewifi.start()
 except:error('Can\'t run sendsavewifi thread in s.py')
 try:
  sendsaveble.start()
 except:error('Can\'t run sendsaveble thread in s.py')
 try:
  scanble.start()
 except:error('Can\'t run scanble thread in s.py')
 try:
  scanwifi.start()
 except:error('Can\'t run scanWifi thread in s.py')
Start()

