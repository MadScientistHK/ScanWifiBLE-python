import os
import time
import sys

def converter(inputfile,outputfile):
    f = open(inputfile,'r')
    res = open(outputfile,'w')
    text = f.readlines()
    i = 0
    for line in text:
        timestamp = float(line[18:-1])
        date = time.ctime(timestamp)
        res.write(line[:-1]+','+str(date)+'\n')
    f.close()
    res.close()
    print 'Done.'

converter(sys.argv[1],sys.argv[2])
