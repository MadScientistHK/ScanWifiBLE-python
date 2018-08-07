import threading
import time
import os
import sys
import bluetooth._bluetooth as bluez
import wifi
import base64
import paho.mqtt.client as mqtt
import socket
import csv
import json
import random
import struct

os.system('sudo systemctl start bluetooth')

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
	    reponse = '{"idp_recieved":"not_recieved_mqtt_broken","mqttip":"81.250.16.95"}'
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
	
	#Open the file to send
        data = []
        if os.path.isfile(file)==True:
            data = open(file,'r')
        txt = data.readlines()
	
	#Check if the file is empty or corrupt
        if txt == [] or len(txt[0]) < 10:
            os.system('sudo rm '+str(file))
            print 'empty file removed'
    except:error('Can\'t send at send(util.py), can\'t open the file :'+str(file))
    
    try:
	#Check if the mqtt is available then sends the data by udp
        if checkMqtt() != False:
            t1 = time.time()
            udp(str(txt[0]),"udpmqttserver.ddns.net")
	    print '\n\n\nSENT BY UDP\n\n\n'
        else:
	#Else it sends the data by http
            t1 = time.time()
	    txt[0] = txt[0].replace("\"","\\\"")
            cmd = "sudo curl -H \"Content-Type: application/json; charset=UTF-8\" -X POST -k -d \"{\\\"toInsert\\\":"+str(txt[0])+"}\" https://c-cada2.mybluemix.net/Positionb64 > reponsemqtt.txt"
            os.system(str(cmd))
	    os.system('sudo rm '+str(file))
	    print '\n\n\nSENT BY HTTP\n\n\n'
        t2 = time.time()
	#Give the seconds it spent to send the data
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

#####################################################################################################
###########################_ON_CONNECT_FUNCTION_#####################################################
#####################################################################################################

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

#####################################################################################################
###########################_ON_MESSAGE_FUNCTION_#####################################################
#####################################################################################################

def on_message(mqttc, obj, msg):
    print(str(msg.payload))
    getFileName(msg.payload)

#####################################################################################################
###########################_ON_PUBLISH_FUNCTION_#####################################################
#####################################################################################################	

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

#####################################################################################################
###########################_ON_SUBSCRIBE_FUNCTION_###################################################
#####################################################################################################

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

#####################################################################################################
###########################_ON_LOG_FUNCTION_#########################################################
#####################################################################################################

def on_log(mqttc, obj, level, string):
    print(string)

#####################################################################################################
###########################_MQTT_LISTENER_FUNCTION_#####################################################
#####################################################################################################

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
###########################_HOW_MANY_FUNCTION_#######################################################
#####################################################################################################
	
def howMany():
    filenames = ['wifi_','ble_']
    dir = os.listdir('/home/pi')
    nb = 0
    for name in dir:
	if 'wifi_' in name or 'ble_' in name:
	    nb=nb+1
    return nb

#####################################################################################################
###########################_SEARCH_WIFI_FUNCTION_####################################################
#####################################################################################################

def Search():
    wifilist = []

    cells = wifi.Cell.all('wlan0')
    for cell in cells:
        wifilist.append(cell)
    return wifilist

#####################################################################################################
###########################_FindFromSearchList_FUNCTION_#############################################
#####################################################################################################

def FindFromSearchList(ssid):
    wifilist = Search()

    for cell in wifilist:
        if cell.ssid == ssid:
            return cell

    return False

#####################################################################################################
###########################_FindFromSavedLis_FUNCTION_###############################################
#####################################################################################################

def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)

    if cell:
        return cell

    return False

#####################################################################################################
###########################_CONNECT_FUNCTION_########################################################
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
###########################_ADD_FUNCTION_############################################################
#####################################################################################################

def Add(cell, password=None):
    if not cell:
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme

#####################################################################################################
###########################_DELETE_FUNCTION_#########################################################
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
###########################_SEARCH_OPEN_WIFI_FUNCTION_###############################################
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
###########################_CONNECT_TO_OPEN_WIFI_FUNCTION_###########################################
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

#####################################################################################################
#####################################################################################################
#####################################################################################################

# BLE iBeaconScanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# JCS 06/07/14

DEBUG = False
# BLE scanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# BLE scanner, based on https://code.google.com/p/pybluez/source/browse/trunk/examples/advanced/inquiry-with-rssi.py

# https://github.com/pauloborges/bluez/blob/master/tools/hcitool.c for lescan
# https://kernel.googlesource.com/pub/scm/bluetooth/bluez/+/5.6/lib/hci.h for opcodes
# https://github.com/pauloborges/bluez/blob/master/lib/hci.c#L2782 for functions used by lescan

# performs a simple device inquiry, and returns a list of ble advertizements 
# discovered device

# NOTE: Python's struct.pack() will add padding bytes unless you make the endianness explicit. Little endian
# should be used for BLE. Always start a struct.pack() format string with "<"

LE_META_EVENT = 0x3e
LE_PUBLIC_ADDRESS=0x00
LE_RANDOM_ADDRESS=0x01
LE_SET_SCAN_PARAMETERS_CP_SIZE=7
OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_PARAMETERS=0x000B
OCF_LE_SET_SCAN_ENABLE=0x000C
OCF_LE_CREATE_CONN=0x000D

LE_ROLE_MASTER = 0x00
LE_ROLE_SLAVE = 0x01

# these are actually subevents of LE_META_EVENT
EVT_LE_CONN_COMPLETE=0x01
EVT_LE_ADVERTISING_REPORT=0x02
EVT_LE_CONN_UPDATE_COMPLETE=0x03
EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE=0x04

# Advertisment event types
ADV_IND=0x00
ADV_DIRECT_IND=0x01
ADV_SCAN_IND=0x02
ADV_NONCONN_IND=0x03
ADV_SCAN_RSP=0x04


def returnnumberpacket(pkt):
    myInteger = 0
    multiple = 256
    for c in pkt:
        myInteger +=  struct.unpack("B",c)[0] * multiple
        multiple = 1
    return myInteger 

def returnstringpacket(pkt):
    myString = "";
    for c in pkt:
        myString +=  "%02x" %struct.unpack("B",c)[0]
    return myString 

def printpacket(pkt):
    for c in pkt:
        sys.stdout.write("%02x " % struct.unpack("B",c)[0])

def get_packed_bdaddr(bdaddr_string):
    packable_addr = []
    addr = bdaddr_string.split(':')
    addr.reverse()
    for b in addr: 
        packable_addr.append(int(b, 16))
    return struct.pack("<BBBBBB", *packable_addr)

def packed_bdaddr_to_string(bdaddr_packed):
    return ':'.join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

def hci_enable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x01)

def hci_disable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x00)

def hci_toggle_le_scan(sock, enable):
# hci_le_set_scan_enable(dd, 0x01, filter_dup, 1000);
# memset(&scan_cp, 0, sizeof(scan_cp));
 #uint8_t         enable;
 #       uint8_t         filter_dup;
#        scan_cp.enable = enable;
#        scan_cp.filter_dup = filter_dup;
#
#        memset(&rq, 0, sizeof(rq));
#        rq.ogf = OGF_LE_CTL;
#        rq.ocf = OCF_LE_SET_SCAN_ENABLE;
#        rq.cparam = &scan_cp;
#        rq.clen = LE_SET_SCAN_ENABLE_CP_SIZE;
#        rq.rparam = &status;
#        rq.rlen = 1;

#        if (hci_send_req(dd, &rq, to) < 0)
#                return -1;
    cmd_pkt = struct.pack("<BB", enable, 0x00)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)


def hci_le_set_scan_parameters(sock):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    SCAN_RANDOM = 0x01
    OWN_TYPE = SCAN_RANDOM
    SCAN_TYPE = 0x01


    
def parse_events(sock, loop_count=100):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # perform a device inquiry on bluetooth device #0
    # The inquiry should last 8 * 1.28 = 10.24 seconds
    # before the inquiry is performed, bluez should flush its cache of
    # previously discovered devices
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
    done = False
    results = []
    myFullList = []
    for i in range(0, loop_count):
        pkt = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", pkt[:3])
        #print "--------------" 
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
		i =0
        elif event == bluez.EVT_NUM_COMP_PKTS:
                i =0 
        elif event == bluez.EVT_DISCONN_COMPLETE:
                i =0 
        elif event == LE_META_EVENT:
            subevent, = struct.unpack("B", pkt[3])
            pkt = pkt[4:]
            if subevent == EVT_LE_CONN_COMPLETE:
                le_handle_connection_complete(pkt)
            elif subevent == EVT_LE_ADVERTISING_REPORT:
                #print "advertising report"
                num_reports = struct.unpack("B", pkt[0])[0]
                report_pkt_offset = 0
                for i in range(0, num_reports):
		
		    if (DEBUG == True):
			print "-------------"
                    	#print "\tfullpacket: ", printpacket(pkt)
		    	print "\tUDID: ", printpacket(pkt[report_pkt_offset -22: report_pkt_offset - 6])
		    	print "\tMAJOR: ", printpacket(pkt[report_pkt_offset -6: report_pkt_offset - 4])
		    	print "\tMINOR: ", printpacket(pkt[report_pkt_offset -4: report_pkt_offset - 2])
                    	print "\tMAC address: ", packed_bdaddr_to_string(pkt[report_pkt_offset + 3:report_pkt_offset + 9])
		    	# commented out - don't know what this byte is.  It's NOT TXPower
                    	txpower, = struct.unpack("b", pkt[report_pkt_offset -2])
                    	print "\t(Unknown):", txpower
	
                    	rssi, = struct.unpack("b", pkt[report_pkt_offset -1])
                    	print "\tRSSI:", rssi
		    # build the return string
                    Adstring = packed_bdaddr_to_string(pkt[report_pkt_offset + 3:report_pkt_offset + 9])
		    Adstring += ","
		    Adstring += returnstringpacket(pkt[report_pkt_offset -22: report_pkt_offset - 6]) 
		    Adstring += ","
		    Adstring += "%i" % returnnumberpacket(pkt[report_pkt_offset -6: report_pkt_offset - 4]) 
		    Adstring += ","
		    Adstring += "%i" % returnnumberpacket(pkt[report_pkt_offset -4: report_pkt_offset - 2]) 
		    Adstring += ","
		    Adstring += "%i" % struct.unpack("b", pkt[report_pkt_offset -2])
		    Adstring += ","
		    Adstring += "%i" % struct.unpack("b", pkt[report_pkt_offset -1])

		    #print "\tAdstring=", Adstring
 		    myFullList.append(Adstring)
                done = True
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    return myFullList

#####################################################################################################
#####################################################################################################
#####################################################################################################

#Start bluetooth interface
os.system('sudo systemctl start bluetooth')

#Scan BLE function, with 1 parameter to count each time it scans
def scanble(comp):
	
    #Initialize bluetooth interface
    dev_id = 0
    try:
    	sock = bluez.hci_open_dev(dev_id)
    except:
	error("error accessing bluetooth device... in ble.py")
    	sys.exit(1)
	
    #Get the serial number of the raspberry to get a unique id
    id = getserial()
	
    #While there is file named "ble_x.json" or "sb_x.json" add +1 to the comp var, to avoid rewritting file or try to send nothing
    while os.path.isfile('ble_'+str(comp)+'.json') == True or os.path.isfile('sb_'+str(comp)+'.json') == True:
        comp=comp+1
	
    #When there is internet connection, it names the new file as "ble_x.csv" and "sb_x.csv" when there is no connection 
    #Idp identify the packet
    if checkInternet() == True:
	file = 'ble_'+str(comp)+'.csv'
	idp = 'ble_'+str(comp)
    else:
	file = 'sb_'+str(comp)+'.csv'
        idp = 'sb_'+str(comp)
    
    #Open a new file with the right name as above
    f = open(file,'w')

    #Used to get the time spent to send the file
    t1 = time.time()

    #Start the event for the scan
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    
    savebeacon = []

    #Return 50 ble scanned
    returnedList = blescan.parse_events(sock,50)
    
    #Second var to get the time spent to send
    t2 = time.time()
    
    #Print how many second it spent to send
    print "scan ble : "+str(t2-t1)
    finalList = []
    
    #Check if a scanned ble is already in the finalList
    for beacon in returnedList:
        if str(beacon[0:17]) not in str(finalList):
	    finalList.append(str(beacon))
	    savebeacon = finalList
		
    #Write the results in the csv file
    for beacon in finalList:
            stamp = time.time()
    	    beacon = beacon.replace("\"","")
            f.write(str(id)+","+str(stamp)+","+beacon+","+idp+"\n")
    f.close()

    #Reopen the file in read mode
    f = open(file,'r')

    #Convert csv to json
    jfile = bcj(file)

    #If there is still internet, send the json file and look back if there is no file that hasn't been sent yet
    if checkInternet() == True:
	send(jfile)
	lookBack(comp)

#Look back if there is no file that hasn't been sent yet
def lookBack(comp):
    if comp == 0:
        i=0
    else:
        i=1
    for i in range(comp):
        time.sleep(1)
        if os.path.isfile('ble_'+str(comp-i)+'.json')== True:
            send('ble_'+str(comp-i)+'.json')
	    print 'i found a lost lamb'

#Scan every 10 seconds
def ble():
    comp=0
    while 1:
        print '\n=========================== Scan BLE Start ==========================\n'
        try:
	    scanble(comp)
	    comp=comp+1
            print comp
	except:error('Error at : '+str(time.time())+' . Can\'t run scanble in ble.py')
        print '\n========================= Scan BLE Complete =========================\n'
        time.sleep(10)

#####################################################################################################
#####################################################################################################
#####################################################################################################

def SearchW(comp):
	
    #Scan every wifi around
    try:
        cells = wifi.Cell.all('wlan0')
    except:error('wlan0 busy, can\'t scan (wif.py)')
    
    #If the program restart, there might be some old files, to avoid to lost them by rewrite, we skip it for the name, and send it later
    try:
    	while os.path.isfile('wifi_'+str(comp)+'.json') == True or os.path.isfile('sw_'+str(comp)+'.json') == True:
	    comp=comp+1
    except:error('Failed to skip the name (wif.py)')
    
    #Changing name in case we lost connection
    try:
    	if checkInternet() == True:
	    file = 'wifi_'+str(comp)+'.csv'
	    idp = "wifi_"+str(comp)
    	else:
	    file = 'sw_'+str(comp)+'.csv'
	    idp = "sw_"+str(comp)
    	id = str(getserial())+','
    	b64 = 'true,'
    except:error('Failed to write the name of the file (wif.py)')
    
    #Create file to send data
    try:
     	f = open(file,'w')
    except:error('Failed to create file for scan (wif.py)')
    
    #Get data of scanning, all the data is in base64 to avoid error about special character
    try:
    	for cell in cells:
	    timestamp = base64.b64encode(str(time.time()))+','
	    bssid = base64.b64encode(str(cell.address))+','
	    channel = base64.b64encode(str(cell.channel))+','
	    rssi = base64.b64encode(str(cell.signal))+','
	    encryption = base64.b64encode(str(cell.encrypted))+','
	    ssid = base64.b64encode(str(cell.ssid))+','
	    if encryption == base64.b64encode('True')+',': chiffrement = base64.b64encode(str(cell.encryption_type))+','
	    else: chiffrement = base64.b64encode('Not protected')+','
	    row = id+timestamp+b64+bssid+channel+rssi+encryption+ssid+chiffrement+idp+'\n'
	    
	    #Writing data
	    try:
      		f.write(row)
	    except:error('Failed to write the file (wif.py)')
    except:error('Failed to collect data (wif.py)')
    
    #Close and open the file to save the data before conversion
    try:
        f.close
        f = open(file,'r')
    except:error('Failed to open the file (wif.py)')
    
    #Convert csv to json
    try:
        jfile = wcj(file)
    except:error('Failed to convert the file (wif.py)')
    
    #Sending the file if there is a internet connection
    try:
	if checkInternet() == True:
    	    send(jfile)
	    try:
		lookBackW(comp) #If it miss a message, it look back to resend missing file
    	    except:error('Failed to send missing file (wif.py)')
    except:error('Failed to send the file (wif.py)')

#If it miss a message, it look back to resend missing file
def lookBackW(comp):
    if comp == 0:
	i=0
    else:
	i=1
    for i in range(comp):
	time.sleep(1)
        if os.path.isfile('wifi_'+str(comp-i)+'.json')== True:
            send('wifi_'+str(comp-i)+'.json')
	    print 'i found a lost lamb'

#Scan wifi every 10 seconds
def w():
    comp = 0
    while 1:
        print "\n=========================== Scan Wifi Start =========================\n"
	try:
            SearchW(comp)
            comp=comp+1
            print comp
        except:error('\n Error at : '+str(time.time())+' . Can\'t run scanWifi in sw.py')
        print "\n========================= Scan Wifi Complete ========================\n"
        time.sleep(10)

#####################################################################################################
#####################################################################################################
#####################################################################################################

#Main function that start every thread to scan bluetooth and wifi, send saves and subscribe to the mqtt server
def Start():
	scanble = threading.Thread(target=ble,args=())
    scanwifi = threading.Thread(target=w,args=())
    sendsaveble = threading.Thread(target=ssb,args=())
    sendsavewifi = threading.Thread(target=ssw,args=())
    mqttlistenerthread = threading.Thread(target=mqttlistener,args=())
    while 1:
        try:
            if mqttlistenerthread.is_alive() == False:
                print 'rerun'
                mqttlistenerthread.start()
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
    	try:
        	if connectopenwifi.is_alive() == False:
        	    print 'openwifi run'
        	    #connectopenwifi.start()
    	except:error('failed to search open wifi')

Start()



