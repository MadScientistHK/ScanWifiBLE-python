import os
os.system('sudo systemctl start bluetooth')
import pygatt
from binascii import hexlify
import time
import binascii
from bluepy import btle
import ibmiotf.device
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        print ("  %s = %s" % (desc, value))
    for udid in dev.getCommonName():
	print ("UDID : " % udid)
