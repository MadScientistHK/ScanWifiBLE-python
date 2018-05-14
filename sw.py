


import time
import os
import csv
from wificsvjson import wcj
from send import send
from checkInternet import checkInternet
from uuid import getnode as get_mac

def scanWifi(comp):
    #Create a file to save the output of the command
    os.system("sudo rm logScan.txt")
    log = open("logScan.txt","w")
    log.close()
    #This command extract some line in iwlist wlan0 scan
    cmd = "sudo iwlist wlan0 scan | awk -F ':' '/Address:/ {print $2,\":\",$3,\":\",$4,\":\",$5,\":\",$6,\":\",$7,\",\";} /ESSID:/ {print $2,\",\";} /Frequency:/ {print $2,\",\";} /level=/ {print $1,\",\";} /Encryption key:/ {print $2,\",\";} /IEEE/ {print $2;} /IE: WPA/ {print $2;}' > logScan.txt"
    os.system(cmd)
    #Re-open the file for read
    log = open("logScan.txt","r")
    #Create an array of each line of the file logScan.txt
    txt = log.readlines()
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
    #Because some wifi doesn't have protection, we resolve the skiping line problem by adding lines
    for k in range(len(txt)):
        if "off" in txt[k]:
            index.insert(0,k+2)
    for h in range(len(index)):
        txt.insert(index[h],"Not_protected")
    #print "hello there"
    for m in range(len(txt)):
        #print txt[m]
        if "on ,\n" == txt[m]:
            index2.insert(0,m+2)
    #print index2
    for t in range(len(index2)):
	#print "doing some shit"
	if index2[t] <= len(txt)-2:
	    if "WPA" not in txt[index2[t]]:
	        #print "i'm doing something with wep"
                txt.insert(index2[t],"WEP")
	    else:pass # print "nothing here captain"
	else :pass
	    #if "WPA" not in txt[index2[t]-1]:
             #   print "i'm doing something with wep"
              #  txt.insert(index2[t],"WEP")
            #else: print "nothing here captain"

    for e in range(len(txt)):
	if "WPA" in txt[e]:
	    if "WPA" in txt[e-1]:
#		print txt[e-1]
#		print txt[e]
		index3.insert(0,e)
#    index3.reverse()
#    print index3
    for r in range(len(index3)):
#	print index3[r]
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
    #Writing the csv
    wifi = open("logWifi.csv", "w")
#   print txt
    #wifi.writerow(["TimeStamp","MAC Address","Frequency(GHz)","Channel","Quality","Signal level(dBm)","Encryption key","ESSID","WPA"])
    savetxt = txt
    while i < nbline:
        stamp = time.time()
	macID = "RPiTest1"
	wifi.write(str(macID)+","+str(stamp)+","+str(txt[i]+txt[i+1]+txt[i+2]+txt[i+3]+txt[i+4]+txt[i+5])+",wifi_"+str(comp)+"\n")
        #print txt[i]+"\n"
	#print str(macID)+","+str(stamp)+","+str(txt[i]+txt[i+1]+txt[i+2]+txt[i+3]+txt[i+4]+txt[i+5])+"\n"
	i=i+6
    wifi.close()
    #print "Scan done, please check the file 'logWifi.csv'"
    wcj('logWifi.csv')
    o=0
    if checkInternet() == True:
        try:
            send('logWifi.json')
        except:
            print 'error while sending'
    else :
	while os.path.isfile('savewifi'+str(o)+'.csv')==True:
	    o=o+1
        savewifi = open('savewifi'+str(o)+'.csv','a')
	p=0
	g=o
        while p < len(savetxt):
            stamp = time.time()
	    diantre = "RPiTest1"
            savewifi.write(str(diantre)+","+str(stamp)+","+str(savetxt[p]+savetxt[p+1]+savetxt[p+2]+savetxt[p+3]+savetxt[p+4]+savetxt[p+5])+",sw_"+str(g)+"\n")
	    p=p+6
        savewifi.close()



def wifi():
  comp = 0
  while 1:
   print "\n=========================== Scan Wifi Start =========================\n"
   scanWifi(comp)
   comp=comp+1
   print "\n========================= Scan Wifi Complete ========================\n"
   time.sleep(10)



