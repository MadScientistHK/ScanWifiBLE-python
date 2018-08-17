import threading
from datetime import datetime
import subprocess
import socket
import urllib
import os
import configparser
import subprocess as sp
os.system('sudo systemctl start bluetooth')
import pygatt
from binascii import hexlify
import time
import binascii
from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate
import paho.mqtt.client as mqtt

SEUIL_TEMPERATURE = 35

def whichConnectedWifi():
    networkInfos = subprocess.check_output(['iwgetid']).split()

    for networkInfo in networkInfos:
        if networkInfo[0:5]=="ESSID":
            info = networkInfo.split('"')
            connectedWifi = info[1]
            return connectedWifi


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


global id,client,a,b,c,d,e,f,g,h,i,j,topic
config = configparser.RawConfigParser()
config.read('mqtt.conf')
id = getserial()
topic = config.get('MQTT','topic')
secure_topic = config.get('MQTT','secure_topic')
broker_address = config.get('MQTT','broker_address')

client = mqtt.Client(id)
client.tls_set("ca.crt")
#client.tls_set("ca2.crt")
client.username_pw_set(config.get('MQTT','username'), config.get('MQTT','password'))
client.connect(broker_address)

#secure_client = mqtt.Client(id + "_secure")
#secure_client.tls_set("ca.crt")
#secure_client.username_pw_set(config.get('MQTT','username'), config.get('MQTT','password'))
#secure_client.connect(broker_address)

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

def checkInternet():
    connected = False
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("www.google.com", 80))
        connected = True
        return connected
    except socket.gaierror:
        print ("Not connected")
        return connected

def writedata(data):
    if checkInternet() == False:
        with open("mydata.json","a") as f:
            f.write(str(data)+',')
            f.close()

def savedata(data):
    with open("/media/usb/mydata.json","a") as f:
        f.write(str(data)+',\n')
        f.close()

def offline(handle,value):
    if checkInternet() == True and os.path.isfile("mydata.json")==True:
        with open("mydata.json","r") as alldata:
            test = str(alldata.read())
            print (test)
            client.publish("sensiLogger", test)
        #os.system('sudo rm mydata.json')
    elif os.path.isfile("mydata.json")==False:
        client.publish("sensiLogger","Pas de tableau a envoyer")

def Luminosity(handle, value):
    lumHex = str(hexlify(value))
    lum = int(lumHex[8:10] + lumHex[6:8],16)
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Luminosity\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(lum)+"\"}"
    #myData={"type":"Luminosity", "id" : id, "timestamp" : tim, "value" : lum}
    client.publish(topic, str(myData))
    writedata(str(myData))
    savedata(str(myData))

def Temperature(handle, value):
    temHex = str(hexlify(value))
    tem = int(temHex[8:10] + temHex[6:8],16)/10
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Temperature\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(tem)+"\"}"
    #myData={"type":"Temperature", "id" : id, "timestamp" : tim, "value" : tem}
    writedata(str(myData))
    savedata(str(myData))
    if tem>SEUIL_TEMPERATURE:
        client.publish(secure_topic,str(myData))
    else:
        client.publish(topic,str(myData))

def Battery(handle, value):
    batHex = str(hexlify(value))
    bat = int(batHex[12:14] +batHex[10:12],16)/1000
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Battery\", \"id\":\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(bat)+"\"}" 
    #myData={"type":"Battery", "id" : id, "timestamp" : tim, "value" : bat}
    client.publish(topic,str(myData))
    writedata(str(myData))
    savedata(str(myData))

def Humidity(handle, value):
    humHex = str(hexlify(value))
    hum = int(humHex[8:10] + humHex[6:8],16)/10
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Humidity\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(hum)+"\"}"
    #myData={"type":"Humidity", "id" : id, "timestamp" : tim, "value" : hum}
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))

def Motion(handle, value):
    motHex = str(hexlify(value))

    tim = int(round(time.time() * 1000))

    accX = int(motHex[8:10] + motHex[6:8],16)/100
    accY = int(motHex[12:14] + motHex[10:12],16)/100
    accZ = int(motHex[16:18] + motHex[14:16],16)/100

    gyrX = int(motHex[20:22] + motHex[18:20],16)
    gyrY = int(motHex[24:26] + motHex[22:24],16)
    gyrZ = int(motHex[28:30] + motHex[26:28],16)

    magX = int(motHex[32:34] + motHex[30:32],16)/100
    magY = int(motHex[36:38] + motHex[34:36],16)/100
    magZ = int(motHex[40:42] + motHex[38:40],16)/100

    myData="{\"type\":\"Accelerometer\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"X\" : \""+str(accX)+"\", \"Y\" : \""+str(accY)+"\", \"Z\" : \""+str(accZ)+"\"}"
    #myData={"type":"Accelerometer", "id" : id, "timestamp" : tim, "X" : accX, "Y" : accY, "Z" : accZ}
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))
    myData="{\"type\":\"Gyroscope\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"X\" : \""+str(gyrX)+"\", \"Y\" : \""+str(gyrY)+"\", \"Z\" : \""+str(gyrZ)+"\"}"
    #myData={"type":"Gyroscope", "id" : id, "timestamp" : tim, "X" : gyrX, "Y" : gyrY, "Z" : gyrZ}
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))
    myData="{\"type\":\"Magnetometer\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"X\" : \""+str(magX)+"\", \"Y\" : \""+str(magY)+"\", \"Z\" : \""+str(magZ)+"\"}"
    #myData={"type": "Magnetometer", "id" : id, "timestamp" : tim, "X" : magX, "Y" : magY, "Z" : magZ}
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))

def Pressure(handle, value):
    preHex = str(hexlify(value))
    pre = int(preHex[12:14] + preHex[10:12] + preHex[8:10] + preHex[6:8],16)/100
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Pressure\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(pre)+"\"}"
    #myData={"type":"Pressure", "id" : id, "timestamp" : tim, "value" : pre}
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))

def Mic_Level(handle, value):
    micHex = str(hexlify(value))
    mic = int(micHex[8:10] + micHex[6:8],16)
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Mic_Level\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(mic)+"\"}"
    #myData={"type":"Mic_Level", "id" : id, "timestamp" : tim, "value" : mic}
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))


def senddata():
    while 1:
        cont = 1
#    secure_client.connect(broker_address)
        client.connect(broker_address)

#    secure_client.loop_start()
        client.loop_start()

        connectedWifi = whichConnectedWifi()

        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(10.0)

        uuid = "00:00:00:00:00:00"

        for dev in devices:
            print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                if value=="SensiBLE":
                    uuid = dev.addr
                print("  %s = %s" % (desc, value))

        print("Connecting...")

        time.sleep(1)

        adapter = pygatt.GATTToolBackend()

        try:
            adapter.start()
            device = adapter.connect(uuid)

            device.subscribe("01000000-0001-11e1-ac36-0002a5d5c51b",callback=Luminosity)
            time.sleep(1)
            device.subscribe("00040000-0001-11e1-ac36-0002a5d5c51b",callback=Temperature)
            time.sleep(1)
            device.subscribe("00020000-0001-11e1-ac36-0002a5d5c51b",callback=Battery)
            time.sleep(1)
            device.subscribe("00080000-0001-11e1-ac36-0002a5d5c51b",callback=Humidity)
            time.sleep(1)
            device.subscribe("00e00000-0001-11e1-ac36-0002a5d5c51b",callback=Motion)
            time.sleep(1)
            device.subscribe("00100000-0001-11e1-ac36-0002a5d5c51b",callback=Pressure)
            time.sleep(1)
            device.subscribe("04000000-0001-11e1-ac36-0002a5d5c51b",callback=Mic_Level)
            time.sleep(1)
            device.subscribe("04000000-0001-11e1-ac36-0002a5d5c51b",callback=offline)

            while cont==1:
                stdoutdata = sp.getoutput("hcitool con")
                if not uuid.upper() in stdoutdata.split() or connectedWifi != whichConnectedWifi():
                    print("not connected")
#                 secure_client.loop_stop()
#                 secure_client.disconnect()
                    client.loop_stop()
                    client.disconnect()
                    cont = 0
                else:
                    print("connected")
        except:
            print("error")
            myData={"error":"Couldn't connect to the sensiBLE"}
            client.publish(topic, str(myData))
#        secure_client.loop_stop()
#        secure_client.disconnect()
            client.loop_stop()
            client.disconnect()
        finally:
            adapter.stop()


#senddata()

