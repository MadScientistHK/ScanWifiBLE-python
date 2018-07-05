import paho.mqtt.client as mqttClient
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
        #hostname = "www.google.com" #example
        #response = os.system("ping -c 1 " + hostname)
        #if response == 1:
            #connected == True
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock.settimeout(1)
        sock.connect(("www.google.com", 80))
	connected = True
        return connected
    except socket.gaierror, e:
        print "Not connected"
    return connected

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
    print msg
    #log = open('logError.txt','a')
    #log.write('\n Error at : '+str(time.time())+' , '+str(msg))
    #log.close()

#####################################################################################################
###########################_SEND_THE_SAVES_OF_THE_WIFI_SCAN_#########################################     
#####################################################################################################

def ssw():
    try:
        i=0
	while 1:
	    max = getfilemax()
	    if checkInternet() == True:
		file = 'sw_'+str(i)+'.json'
            	if os.path.isfile(file)==True and i <= max:
		    send(file)
	        i=i+1
		if i > max:i=0
    except:error('can not send savewifi')

#####################################################################################################
###########################_SEND_THE_SAVES_OF_THE_BLE_SCAN_##########################################     
#####################################################################################################

def ssb():
    try:
        i=0
        while 1:
	    max = getfilemax()
            if checkInternet() == True:
                file = 'sb_'+str(i)+'.json'
                if os.path.isfile(file)==True and i <= max:
                    send(file)
                i=i+1
		if i > max:i=0
    except:error('can not send saveble')

#####################################################################################################
###########################_THE_SEND_FUNCTION__######################################################     
#####################################################################################################

def send(file):
    try:
	data = []
	if os.path.isfile(file)==True:
            data = open(file,'r')
        txt = data.readlines()
    	if txt == [] or len(txt) < 10:
            os.system('sudo rm '+str(file))
	    print 'empty file removed'
    	else:
            txt[0] = txt[0].replace("\"","\\\"")
    except:error('Can\'t send at send(util.py), can\'t open the file :'+str(file))
    try:
	t1 = time.time()
	#topic = "8aed96ca0f22ea24fefaa5ccce827c04"
	udp(str(txt[0]),5100,'81.250.16.95')
	#msg = subscribe.simple(topic, hostname="81.250.16.95", port=1883, auth={'username':'Admin_HearAndKnow','password':'DeVinci2018'})
	#print("%s %s" % (msg.topic, msg.payload))
        #t1 = time.time()
        #cmd = "sudo curl -H \"Content-Type: application/json; charset=UTF-8\" -X POST -k -d \"{\\\"toInsert\\\":"+str(txt[0])+"}\" https://c-cada2.mybluemix.net/Positionb64"
        #os.system(str(cmd))
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

def udp(data, port=5100, addr='81.250.16.95'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
    s.sendto(data, (addr, port))

#####################################################################################################
###########################_MQTT_ON_CONNECT_CALLBACK_FUNCTION_#######################################     
#####################################################################################################

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")

#####################################################################################################
###########################_MQTT_ON_MESSAGE_CALLBACK_FUNCTION_#######################################
#####################################################################################################

def on_message(client, userdata, message):
    print "Message received: "  + message.payload
    filenames = ['wifi_','ble_','sw_','sb_']
    i=5
    num = ' '
    list = os.listdir('/home/pi')
    for name in filenames:
    	if  message.payload.find(name) != -1:
	    while '"' not in message.payload[message.payload.find(name):message.payload.find(name)+i]:
            	i=i+1
            	num = message.payload[message.payload.find(name):message.payload.find(name)+i-1] # os.system('sudo rm '+str(message.payload[message.payload.find(str_wifi):message.payload.find(str_wifi)+i-1]))
	    os.system('sudo rm '+str(num)+'.json')

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_##################################################
#####################################################################################################

def mqttlistner():
    Connected = True   #global variable for the state of the connection
    broker_address= "81.250.16.95"      #Broker address
    port = 1883                         #Broker port
    user = "Admin_HearAndKnow"          #Connection username
    password = "DeVinci2018"
    topic = "8aed96ca0f22ea24fefaa5ccce827c04"         #Connection password
    client = mqttClient.Client("Python")               #create new instance
    client.username_pw_set(user, password=password)    #set username and password 
    client.on_connect= on_connect                      #attach function to callback
    client.on_message= on_message                      #attach function to callback
    client.qos=1
    client.connect(broker_address, port=port)          #connect to broker
    client.loop_start()        #start the loop
    while Connected != True:    #Wait for connection
        time.sleep(0.1)
    client.subscribe(topic)
    try:
    	while True:
            time.sleep(1)
    except KeyboardInterrupt:
    	print "exiting"
    	client.disconnect()
    	client.loop_stop()



