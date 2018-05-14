import csv
import json
import sys
import os


def wcj(file):
 csvfile = open(file, 'r')
 jfile = file[:-3]+"json"
 jsonfile = open(jfile, 'w')
 reader = csv.DictReader(csvfile,("ID","TimeStamp","BSSID","frequency","Channel","RSSI","EncryptionKey","SSID","Chiffrement","idp"))
 out = json.dumps( [ row for row in reader ] )
 jsonfile.write(out)
 
