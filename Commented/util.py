import paho.mqtt.client as mqtt
import socket
import csv
import json
import sys
import threading
import time
import os
import wifi
import random

#####################################################################################################
###########################_CHECK_THE_INTERNET_CONNECTION_###########################################
#####################################################################################################

def checkInternet():
    hostname = "www.google.com"
    response = os.system("sudo ping -q -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False

    return pingstatus

#####################################################################################################
###########################_MQTT_CHECK_FUNCTION_#####################################################
#####################################################################################################

def checkMqtt():
    hostname = "udpmqttserver.ddns.net"
    print hostname
    response = os.system("sudo ping -q -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False

    return pingstatus

#####################################################################################################
###########################_SEARCH_IF_THERE_IS_NUMBER_IN_A_STRING_###################################
#####################################################################################################

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

#####################################################################################################
###########################_RETURN_THE_NUMBER_MAX_OF_NAME_FILE_######################################
#####################################################################################################

def getfilemax():
    try:
    	list = os.listdir('/home/pi')
    	max = 0
    	for file in list:
	    if hasNumbers(str(file))==True:
	    	if max < int(filter(str.isdigit,str(file))):
	    	    max = int(filter(str.isdigit,str(file)))
    	return max
    except:error('can not get the max')

#####################################################################################################
###########################_WRITE_LOG_IF_ERROR_######################################################
#####################################################################################################

def error(msg):
    a=0
    #print msg
    #log = open('logError.txt','a')
    #log.write('\n Error at : '+str(time.time())+' , '+str(msg))
    #log.close()

#####################################################################################################
###########################_SEND_THE_SAVES_OF_THE_WIFI_SCAN_#########################################
#####################################################################################################

def ssw():
    try:
        print "ssw running"
        i=0
        max = getfilemax()
        while 1:
            file = 'sw_'+str(i)+'.json'
            if os.path.isfile(file)==True and i <= max:
                if checkInternet() == True:
                    send(file)
                    print "sending save WIFI"
            i=i+1
            #print i
            if i > max:i=0
    except:error('can not send savewifi')

#####################################################################################################
###########################_SEND_THE_SAVES_OF_THE_BLE_SCAN_##########################################
#####################################################################################################

def ssb():
    try:
        print "ssb running"
        i=0
        max = getfilemax()
        while 1:
            file = 'sb_'+str(i)+'.json'
            if os.path.isfile(file)==True and i <= max:
                if checkInternet() == True:
                    send(file)
                    print "sending save BLE"
            i=i+1
            #print i
            if i > max:i=0
    except:error('can not send saveble')

#####################################################################################################
###########################_GET_FILE_NAME_FUNCTION_##################################################     
#####################################################################################################

def getFileName(message):
    filenames = ['wifi_','ble_','sw_','sb_']
    num = ' '
    list = os.listdir('/home/pi')
    for name in filenames:
        i=len(name)
        if  message.find(name) != -1:
            while '"' not in message[message.find(name):message.find(name)+i]:
                i=i+1
                num = message[message.find(name):message.find(name)+i-1]
            os.system('sudo rm '+str(num)+'.json')

#####################################################################################################
###########################_GET_MQTTIP_FUNCTION_#####################################################     
#####################################################################################################

def getMqttIp():
    print 'GET MQTT IP'
    name = 'mqttip":"'
    reponse = ' '
    try:
	if os.path.isfile('reponsemqtt.txt') == True:
	    f=open('reponsemqtt.txt','r')
	    reponse = f.readline()
	    f.close()
	if len(reponse) < 2 :
	    reponse = '{"idp_recieved":"not_recieved_mqtt_broken","mqttip":"81.250.16.95"'
	    #os.system('sudo rm reponsemqtt.txt')
    except:
	error('can not open the file reponsemqtt.txt')
    i=0
    ip=' '
    if reponse.find(name) != -1:
        while '"' not in reponse[reponse.find(name)+9:reponse.find(name)+9+i]:
            i=i+1
            ip = reponse[reponse.find(name)+9:reponse.find(name)+9+i-1]
    return ip

#####################################################################################################
###########################_THE_SEND_FUNCTION__######################################################     
#####################################################################################################

def send(file):
    try:
        data = []
        if os.path.isfile(file)==True:
            data = open(file,'r')
        txt = data.readlines()
        if txt == [] or len(txt[0]) < 10:
            os.system('sudo rm '+str(file))
            print 'empty file removed'
    except:error('Can\'t send at send(util.py), can\'t open the file :'+str(file))
    try:
        if checkMqtt() != False:
            t1 = time.time()
            udp(str(txt[0]),"udpmqttserver.ddns.net")
	    print '\n\n\nSENT BY UDP\n\n\n'
        else:
            t1 = time.time()
	    txt[0] = txt[0].replace("\"","\\\"")
            cmd = "sudo curl -H \"Content-Type: application/json; charset=UTF-8\" -X POST -k -d \"{\\\"toInsert\\\":"+str(txt[0])+"}\" https://c-cada2.mybluemix.net/Positionb64 > reponsemqtt.txt"
            os.system(str(cmd))
	    os.system('sudo rm '+str(file))
	    print '\n\n\nSENT BY HTTP\n\n\n'
        t2 = time.time()
        print 'send : '+str(t2-t1)
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
    	    reader = csv.DictReader(csvfile,("ID","TimeStamp","b64","BSSID","channel","RSSI","EncryptionKey","SSID","Chiffrement","idp"))
    	    out = json.dumps( [ row for row in reader ] )
    	    jsonfile.write(out)
	    os.system('sudo rm '+file)
	    return jfile
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
	    os.system('sudo rm '+file)
            return jfile
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

def udp(data, addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
    s.sendto(data, (addr, 5100))






def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print(str(msg.payload))
    getFileName(msg.payload)

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

def mqttlistener():
    mqttc = mqtt.Client()
    ip = getMqttIp()
    broker_address = str(ip)  # "udpmqttserver.ddns.net" # str(ip)
    user = "rasp2"
    password = "DeVinci2018"
    topic = "8aed96ca0f22ea24fefaa5ccce827c04/#" #+str(getserial())
    mqttc.username_pw_set(user, password=password)
    mqttc.qos=2
    mqttc.tls_set("ca.crt")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.connect(broker_address, 1883)
    mqttc.subscribe(topic)
    mqttc.loop_forever(1)

#####################################################################################################
###########################_MQTT_ON_CONNECT_CALLBACK_FUNCTION_#######################################     
#####################################################################################################

def Pon_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")

#####################################################################################################
###########################_MQTT_ON_MESSAGE_CALLBACK_FUNCTION_#######################################
#####################################################################################################

def Pon_message(client, userdata, message):
    print "Message received: "  + message.payload
    getFileName(message.payload)

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_##################################################
#####################################################################################################

def Pmqttlistener():
	print howMany()
    	Connected = True   #global variable for the state of the connection
    	ip = getMqttIp()
    	broker_address= str(ip)      #Broker address
    	port = 1883                         #Broker port
    	user = "rasp2" # +str(random.randint(0,100000000))          #Connection username
    	password = "DeVinci2018"
    	topic = "8aed96ca0f22ea24fefaa5ccce827c04"         #Connection password
    	client = mqttClient.Client("Rasp2"+str(random.randint(0,100000000)))               #create new instance
    	client.username_pw_set(user, password=password)    #set username and password 
    	client.on_connect= on_connect                      #attach function to callback
    	client.on_message= on_message                      #attach function to callback
    	client.qos=2
    	client.connect(broker_address, port)          #connect to broker
    	client.loop_start()       #start the loop
    	while Connected != True:    #Wait for connection
            time.sleep(0.1)
    	client.subscribe(topic)
    	try:
    	    while True:
		time.sleep(1)
    	except:
    	    print "exiting"
    	    client.disconnect()
    	    client.loop_stop()
	    mqttlistener()



def howMany():
    filenames = ['wifi_','ble_']
    dir = os.listdir('/home/pi')
    nb = 0
    for name in dir:
	if 'wifi_' in name or 'ble_' in name:
	    nb=nb+1
    return nb

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_##################################################
#####################################################################################################

def Search():
    wifilist = []

    cells = wifi.Cell.all('wlan0')
    for cell in cells:
        wifilist.append(cell)
        #print( str(cell.ssid)+", " )
    return wifilist

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_##################################################
#####################################################################################################

def FindFromSearchList(ssid):
    wifilist = Search()

    for cell in wifilist:
        if cell.ssid == ssid:
            return cell

    return False

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_##################################################
#####################################################################################################

def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)

    if cell:
        return cell

    return False

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_##################################################
#####################################################################################################

def Connect(ssid, password=None):
    cell = FindFromSearchList(ssid)

    if cell:
        savedcell = FindFromSavedList(cell.ssid)

        # Already Saved from Setting
        if savedcell:
            savedcell.activate()
            return cell

        # First time to connect
        else:
            if cell.encrypted:
                if password:
                    scheme = Add(cell, password)

                    try:
                        scheme.activate()

                    # Wrong Password
                    except wifi.exceptions.ConnectionError:
                        Delete(ssid)
                        return False

                    return cell
                else:
                    return False
            else:
                scheme = Add(cell)

                try:
                    scheme.activate()
                except wifi.exceptions.ConnectionError:
                    Delete(ssid)
                    return False

                return cell

    return False

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_##################################################
#####################################################################################################

def Add(cell, password=None):
    if not cell:
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_##################################################
#####################################################################################################

def Delete(ssid):
    if not ssid:
        return False

    cell = FindFromSavedList(ssid)

    if cell:
        cell.delete()
        return True

    return False

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_##################################################
#####################################################################################################

def Search_open():
    wifilist = Search()
    wifiopenlist = []
    i=0
    for i in range(len(wifilist)):
        if wifilist[i].encrypted == False:
            wifiopenlist.append(str(wifilist[i].ssid))
    return wifiopenlist

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_##################################################
#####################################################################################################

def openWifi():
    try:
        while 1:
            #print 'before checkinternet'
            if checkInternet() == False:
                #print 'after checkinternet'
                result = Search_open()
              #  f = open('logOpen.txt','a')
                i =0
             #   f.write('results : '+str(result)+'\n')
                for i in range(len(result)):
                  #  f.write('try to connect to : '+str(result[i])+'\n')
                    try:
                        Connect(str(result[i]))
                    except:a=0 #  f.write('failed to connect : '+str(result[i])+'\n')
                   # f.write('connecting to : '+str(result[i])+'\n')
                   # f.write('waiting 3s : '+str(result[i])+'\n')
                    if checkInternet() == True:
                  #      f.write('success to connect to : '+str(result[i])+'\n')
                        break
                 #       f.write('Login page at : '+str(result[i])+'\n')
                #f.close()
            else:
                time.sleep(3)
    except:print "Failed"




