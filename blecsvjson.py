import csv
import json
import sys

def bcj(file): 
 csvfile = open(file, 'r')
 jfile = file[:-3]+"json"
 jsonfile = open(jfile, 'w')
 fieldnames = ("ID","TimeStamp","MAC","UDID","Minor","Major","TX","RSSI")
 reader = csv.DictReader(csvfile,fieldnames)
 out = json.dumps( [ row for row in reader ] )
 jsonfile.write(out)
 
