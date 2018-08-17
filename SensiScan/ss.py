import sys
import wifi
import base64
import csv
import json
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

#Get the serial number of the raspberry pi
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

#MQTT parameters, if you need to edit, use the file mqtt.conf
global id,client,a,b,c,d,e,f,g,h,i,j,topic
config = configparser.RawConfigParser()
config.read('mqtt.conf')
id = str(getserial())
topic = config.get('MQTT','topic')
secure_topic = config.get('MQTT','secure_topic')
broker_address = config.get('MQTT','broker_address')
client = mqtt.Client(id)

#To change the certificat for the mqtt server, replace the older one, or create a new one and uncomment the line below :
#client.tls_set("Name_of_your_certificat.crt")

client.tls_set("ca.crt")
#client.tls_set("ca2.crt")

client.username_pw_set(config.get('MQTT','username'), config.get('MQTT','password'))
client.connect(broker_address)

#Create directory in the working directory and usb stick to save data
if os.path.isdir("/home/pi/Data") != True:
    os.system("sudo mkdir /home/pi/Data")
try:
    if os.path.isdir("/media/usb/Data") != True:
        os.system("sudo mkdir /media/usb/Data")
except:error("usb stick unmounted")

#Return True or False, if there a internet connection or not
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

#Encode string to base64
def ToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

#Search if there is a number in a string
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

#Print error for debug
def error(msg):
    print (msg)
    #log = open('logError.txt','a')
    #log.write('\n Error at : '+str(time.time())+' , '+str(msg))
    #log.close()

#Convert wifi.csv file to .json file
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

#Scan all the wifi around and save it in bsae64 in csv, then it's convert to json
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
        file = '/home/pi/Data/sw_'+str(comp)+'.csv'
        idp = "sw_"+str(comp)
        #id = str(getserial())
        b64 = 'true'
    except:error('Failed to write the name of the file (wif.py)')

    #Create file to send data
    try:
        print (file)
        z = open(file,'w')
    except:error('Failed to create file for scan (wif.py)')

    #Get data of scanning, all the data is in base64 to avoid error about special character
    try:
        for cell in cells:
            print (cell)
            timestamptmp = str(time.time())
            timestamp = ToBase64(timestamptmp)
            bssidtmp = str(cell.address)
            bssid = ToBase64(bssidtmp)
            channeltmp = str(cell.channel)
            channel = ToBase64(channeltmp)
            rssitmp = str(cell.signal)
            rssi = ToBase64(rssitmp)
            encryptiontmp = str(cell.encrypted)
            encryption = ToBase64(encryptiontmp)
            ssidtmp = str(cell.ssid)
            ssid = ToBase64(ssidtmp)
            if encryption == ToBase64('True'):
                chiffrementtmp = str(cell.encryption_type)
                chiffrement = ToBase64(chiffrementtmp)
            else: chiffrement = ToBase64('Not protected')
            rowtmp = str(id)+','+str(timestamp)+','+str(b64)+','+str(bssid)+','+str(channel)+','+str(rssi)+','+str(encryption)+','+str(ssid)+','+str(chiffrement)+','+str(idp)+'\n'
            #Writing data
            rowtmp2 = rowtmp.replace("b'","")
            row = rowtmp2.replace("'","")
            #print (row)
            try:
                 z.write(row)
            except:error('Failed to write the file (wif.py)')
    except:error('Failed to collect data (wif.py)')

    #Close and open the file to save the data before conversion
    try:
        z.close
        z = open(file,'r')
    except:error('Failed to open the file (wif.py)')

    #Convert csv to json
    try:
        jfile = wcj(file)
    except:error('Failed to convert the file (wif.py)')

    #Sending the file if there is a internet connection
    try:
        os.system("sudo cp "+jfile+" /media/usb/Data")
    except:error("usb stick unmounted")


#Scan wifi every 10 seconds
def w():
    comp = 0
    while 1:
        print ("\n=========================== Scan Wifi Start =========================\n")
        try:
            SearchW(comp)
            comp=comp+1
            print (comp)
        except:error('\n Error at : '+str(time.time())+' . Can\'t run scanWifi in sw.py')
        print ("\n========================= Scan Wifi Complete ========================\n")
        time.sleep(10)


def whichConnectedWifi():
    networkInfos = subprocess.check_output(['iwgetid']).split()

    for networkInfo in networkInfos:
        if networkInfo[0:5]=="ESSID":
            info = networkInfo.split('"')
            connectedWifi = info[1]
            return connectedWifi

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

#Saves all the captors' data in the working directory if there is no internet connection
def writedata(data):
    if checkInternet() == False:
        with open("mydata.json","a") as f:
            f.write(str(data)+',')
            f.close()

#Saves all the captors' data in the usb stick as a historic
def savedata(data):
    with open("/media/usb/mydata.json","a") as f:
        f.write(str(data)+',\n')
        f.close()

#If there is a save file in the working directory, send it when connection is available
def offline(handle,value):
    if checkInternet() == True and os.path.isfile("mydata.json")==True:
        with open("mydata.json","r") as alldata:
            test = str(alldata.read())
            print (test)
            client.publish("sensiLogger", test)
        os.system('sudo rm mydata.json')
    elif os.path.isfile("mydata.json")==False:
        client.publish("sensiLogger","Pas de tableau a envoyer")

#Get the luminosity value
def Luminosity(handle, value):
    lumHex = str(hexlify(value))
    lum = int(lumHex[8:10] + lumHex[6:8],16)
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Luminosity\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(lum)+"\"}"
    client.publish(topic, str(myData))
    writedata(str(myData))
    savedata(str(myData))

#Get the temperature value
def Temperature(handle, value):
    temHex = str(hexlify(value))
    tem = int(temHex[8:10] + temHex[6:8],16)/10
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Temperature\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(tem)+"\"}"
    writedata(str(myData))
    savedata(str(myData))
    client.publish(topic,str(myData))

#Get the battery level
def Battery(handle, value):
    batHex = str(hexlify(value))
    bat = int(batHex[12:14] +batHex[10:12],16)/1000
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Battery\", \"id\":\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(bat)+"\"}" 
    client.publish(topic,str(myData))
    writedata(str(myData))
    savedata(str(myData))

#Get the humidity value
def Humidity(handle, value):
    humHex = str(hexlify(value))
    hum = int(humHex[8:10] + humHex[6:8],16)/10
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Humidity\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(hum)+"\"}"
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))

#Get the accelerometer, gyroscope and magnetometer values
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
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))
    myData="{\"type\":\"Gyroscope\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"X\" : \""+str(gyrX)+"\", \"Y\" : \""+str(gyrY)+"\", \"Z\" : \""+str(gyrZ)+"\"}"
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))
    myData="{\"type\":\"Magnetometer\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"X\" : \""+str(magX)+"\", \"Y\" : \""+str(magY)+"\", \"Z\" : \""+str(magZ)+"\"}"
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))

#Get the pressure value
def Pressure(handle, value):
    preHex = str(hexlify(value))
    pre = int(preHex[12:14] + preHex[10:12] + preHex[8:10] + preHex[6:8],16)/100
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Pressure\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(pre)+"\"}"
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))

#Get the mic level
def Mic_Level(handle, value):
    micHex = str(hexlify(value))
    mic = int(micHex[8:10] + micHex[6:8],16)
    tim = int(round(time.time() * 1000))
    myData="{\"type\":\"Mic_Level\", \"id\" :\""+str(id)+"\", \"timestamp\" : \""+str(tim)+"\", \"value\" : \""+str(mic)+"\"}"
    client.publish(topic,  str(myData))
    writedata(str(myData))
    savedata(str(myData))

#Connect to the sensiBLE, to the mqtt server and send all the data of the captors
def senddata():
    while 1:
        cont = 1
        client.connect(broker_address)
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
                    client.loop_stop()
                    client.disconnect()
                    cont = 0
                else:
                    print("connected")
        except:
            print("error")
            myData={"error":"Couldn't connect to the sensiBLE"}
            client.publish(topic, str(myData))
            client.loop_stop()
            client.disconnect()
        finally:
            adapter.stop()

#Launch wifi scan and sensible thread
def launcher():
    wifi_thread = threading.Thread(target=w,args=())
    sensi_thread = threading.Thread(target=senddata,args=())
    while 1:
        if wifi_thread.is_alive() == False:
            wifi_thread.start()
        if sensi_thread.is_alive() == False:
            sensi_thread.start()

launcher()
