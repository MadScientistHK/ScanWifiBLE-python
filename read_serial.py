#!/usr/bin/env python
import time
import serial
import os
import csv

#Initialisation du port qu'on veut ecouter
ser = serial.Serial(
 port='/dev/ttyACM0',
 baudrate = 115200,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)

#Get les valeurs des differents capteurs
def Wizi():
    count = 0
    ok = 0
    while 1:
        if (count > 100):
            x=ser.readline()
	    ok = 1
            print x
            ts = time.time()
            if 'Mag' in x:
                x=x.replace('Mag ','')
                mag = open("MAG.csv","a")
                mag.write(str(ts)+','+str(x))
                mag.close()
            if 'Acc' in x:
                x=x.replace('Acc ','')
                acc = open("ACC.csv","a")
                acc.write(str(ts)+','+str(x))
                acc.close()
            if 'Pre' in x:
                x=x.replace('Pre ','')
                pre = open("PRE.csv","a")
                pre.write(str(ts)+','+str(x))
                pre.close()
            if 'Hum' in x:
                x=x.replace('Hum ','')
                hum = open("HUM.csv","a")
                hum.write(str(ts)+','+str(x))
                hum.close()
            if 'Tem' in x:
                x=x.replace('Tem ','')
                tem = open("TEM.csv","a")
                tem.write(str(ts)+','+str(x))
                tem.close()
            if 'Lig' in x:
                x=x.replace('Lig ','')
                lig = open("LIG.csv","a")
                lig.write(str(ts)+','+str(x))
                lig.close()            
        if(ok==0):
            count=count+1

Wizi()
