# encoding: utf-8

import base64
import time
import os
import csv
from util import *

def scanWifi(comp):
    #Create a file to save the output of the command
    os.system("sudo rm logScan.txt")
    source = open("logScan.txt","w")
    source.close()
    #This command extract some line in iwlist wlan0 scan
    cmd = "sudo iwlist wlan0 scan | awk -F ':' '/Address:/ {print $2,\":\",$3,\":\",$4,\":\",$5,\":\",$6,\":\",$7,\",\";} /ESSID:/ {print $2,\",\";} /Frequency:/ {print $2,\",\";} /level=/ {print $1,\",\";} /Encryption key:/ {print $2,\",\";} /IEEE/ {print $2;} /IE: WPA/ {print $2;}' > logScan.txt"
    os.system(cmd)
    #Re-open the file for read
    source = open("logScan.txt","r")
    #Create an array of each line of the file logScan.txt
    txt = source.readlines()
    #Need some var
    i=0
    j=0
    k=0
    m=0
    t=0
    h=0
    e=0
    r=0
    t=0
    index=[]
    index2=[]
    index3=[]
    #Because some wifi doesn't have protection, we resolve the skiping line problem by adding 'Not protected'
    for k in range(len(txt)):
        if "off" in txt[k]:
            index.insert(0,k+2)
    for h in range(len(index)):
        txt.insert(index[h],"Not_protected")
    #Some has encryyption key at 'on' but nothing is print, it's a WEP 
    for m in range(len(txt)):
        if "on ,\n" == txt[m]:
            index2.insert(0,m+2)
    for t in range(len(index2)):
	if index2[t] <= len(txt)-2:
	    if "WPA" not in txt[index2[t]]:
                txt.insert(index2[t],"WEP")
    #Some has more than one encryption, we only take the first one
    for e in range(len(txt)):
	if "WPA" in txt[e]:
	    if "WPA" in txt[e-1]:
		index3.insert(0,e)
    for r in range(len(index3)):
	if index3 != []:
	    del txt[index3[r]]
    #Conversion .txt to .csv
    for j in range(len(txt)):
	txt[j] = txt[j].replace('\n','')
	txt[j] = txt[j].replace(' ','')
	if j%6==5:
            txt[j]=txt[j].replace('IEEE802.11','')
        if j%6==4:
	    txt[j]=txt[j].replace('"','')
	if j%6==2:
	    txt[j]=txt[j].replace('Quality=','')
	    txt[j]=txt[j].replace('/70 Signallevel=','')
	    txt[j]=txt[j].replace('dBm','')
	    txt[j]=txt[j][-4:]
	if j%6==1:
	    txt[j]=txt[j].replace('GHz(Channel',',')
	    txt[j]=txt[j].replace(')','')
    nbline =  len(txt)
    i=0
    #Encode in b64 because we need to handle special character
    for i in range(len(txt)):
        txt[i] = base64.b64encode(txt[i])+","
    #For save the scan
    savetxt = txt
    #Writing the csv
    wifi = open("logWifi.csv", "w")
    i=0
    while i < nbline:
        stamp = time.time()
	macID = getserial()
	try:
	    wifi.write(str(macID)+","+str(stamp)+",true,"+str(txt[i]+txt[i+1]+txt[i+2]+txt[i+3]+txt[i+4]+txt[i+5])+"wifi_"+str(comp)+"\n")
	except:error("Can't write logWifi.csv because sth wrong happend in the scan in sw.py")
	#print str(macID)+","+str(stamp)+",true,"+str(txt[i]+txt[i+1]+txt[i+2]+txt[i+3]+txt[i+4]+txt[i+5])+"wifi_"+str(comp)+"\n"
	i=i+6
    wifi.close()
    #Convert from csv to json
    wcj('logWifi.csv')
    o=0
    #Send or save if internet connection or not
    if checkInternet() == True:
        try:
            send('logWifi.json')
        except:error('error while sending in sw.py')
    else :
	while os.path.isfile('savewifi'+str(o)+'.csv')==True:
	    o=o+1
        savewifi = open('savewifi'+str(o)+'.csv','a')
	p=0
	g=o
        while p < len(savetxt):
            stamp = time.time()
	    diantre = getserial()
	    try:
            	savewifi.write(str(diantre)+","+str(stamp)+",true,"+str(savetxt[p]+savetxt[p+1]+savetxt[p+2]+savetxt[p+3]+savetxt[p+4]+savetxt[p+5])+",sw_"+str(g)+"\n")
	    except:error("Can't write savewifi_x_.csv because sth wrong happend in the scan in sw.py")
	    p=p+6
        savewifi.close()



def wifi():
  comp = 0
  while 1:
   print "\n=========================== Scan Wifi Start =========================\n"
   try:
    scanWifi(comp)
    comp=comp+1
   except:
    log = open('logError.txt','a')
    log.write('\n Error at : '+str(time.time())+' . Can\'t run scanWifi in sw.py')
    log.close()
   print "\n========================= Scan Wifi Complete ========================\n"
   time.sleep(10)



