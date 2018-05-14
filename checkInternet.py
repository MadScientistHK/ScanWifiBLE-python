
import socket

 
def checkInternet():
 connected = False
 try:
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect(("www.google.com", 80))
  connected = True
  return connected
 except socket.gaierror, e:
  print "Not connected"
  return connected
