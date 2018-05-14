import csv
import json
import sys

csvfile = open(sys.argv[1], 'r')
jsonfile = open(sys.argv[2], 'w')

print csvfile
print jsonfile

fieldnames = ("TimeStamp","MAC","UDID","Minor","Major","TX","RSSI")
print fieldnames
reader = csv.DictReader(csvfile,fieldnames)
out = json.dumps( [ row for row in reader ] )
jsonfile.write(out)
