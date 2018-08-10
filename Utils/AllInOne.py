import os
from progress.bar import Bar
import time
import csv
import json
import base64

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def getfilemax():
    try:
    	list = os.listdir(os.getcwd())
    	max = 0
    	for file in list:
	    if hasNumbers(str(file))==True:
	    	if max < int(filter(str.isdigit,str(file))):
	    	    max = int(filter(str.isdigit,str(file)))
    	return max
    except:error('can not get the max')

def deb64(file):
    try:
        f = open(file,"r")
        data = f.readlines()
        f.close()
        g = open("all.csv","w")
        count = 0
        for row in data:
            if count == 0:
                g.write(str(row[:-1]))
                count += 1
            else:
                strings = row.split(",")
                for element in strings:
                    if element == 'true' or element == 'Not protected' or "000000" in element:
                        g.write(element+',')
                    elif 'sw_' in element or 'wifi_' in element:
                        g.write(element+',')
                    else:
                        g.write(base64.b64decode(element)+',')
            g.write('\n')
        g.close()
        os.remove("tmp.csv")
    except:
        print "ERROR deb64!"

def gathering():
    i=0
    path=os.getcwd()
    first = True
    max=getfilemax()
    bar = Bar("Processing",suffix='%(percent)d%%',max=max-5)
    try:
        f = open("all.json","w")
        c = open("tmp.csv","w")
        csvwriter = csv.writer(c)
        csvwriter.writerow(['Chiffrement','SSID','BSSID','b64','TimeStamp','IDP','SerialNumber','RSSI','Encryption','Channel'])
        for i in range(max+1):
            if os.path.isfile(str(path)+"/sw_"+str(i)+".json") == True:
                g = open(str(path)+"/sw_"+str(i)+".json","r")
                data=g.readline()
                if len(data) > 20:
                    parseData=json.loads(data)
                    count = 0
                    for row in parseData:
                        csvwriter.writerow(row.values())
                    if first == True:
                        first = False
                        f.write("[\n{\"toInsert\":\""+data+"\"},")
                    elif i == max-1:
                        f.write("\n{\"toInsert\":\""+data+"\"}\n]")
                    else:
                        f.write("\n{\"toInsert\":\""+data+"\"},")
                    bar.next()
                    g.close()
        bar.finish()
        f.close()
        c.close()
        deb64('tmp.csv')
    except:
        print 'It didn\'t worked'
    print "Done."
    time.sleep(3)

gathering()
