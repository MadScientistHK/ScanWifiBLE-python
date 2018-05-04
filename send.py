import os
import sys
def send(file):
 data = open(file,'r')
 txt = data.readlines()
 txt[0] = txt[0].replace("\"","\\\"")

 try:
  cmd = "sudo curl -H \"Content-Type: application/json; charset=UTF-8\" -X POST -k -d \"{\\\"toInsert\\\":"+str(txt[0])+"}\" https://c-cada2.mybluemix.net/InsertManyData"
  os.system(str(cmd))
 except:
  print 'No connection'
