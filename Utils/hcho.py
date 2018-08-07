import grovepi
import math
import csv
from time import time,sleep
sound_sensor =2 
hcho_sensor = 0
led = 5
grovepi.pinMode(hcho_sensor,"INPUT")
grovepi.pinMode(sound_sensor,"INPUT")
grove_vcc = 4.95

R0=18.60


def write_csv(data):
    with open('sensordata.csv', 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)

def gaz():
    while True:
	try:
	# Get sensor value
		sound_value = grovepi.analogRead(sound_sensor)
		#print("sound_value = %d" %sound_value)
		sensor_value = grovepi.analogRead(hcho_sensor)
		voltage =(float)( sensor_value * grove_vcc/1024)
		RS=(1023.0/sensor_value)-1
		ppm = 10 ** ((math.log10(RS/R0) -0.0827) / (-0.4807))
		print(time(),"sensor_value =", sensor_value, " voltage =", voltage, "R0=", R0, "RS=", RS, "HCHO ppm", ppm)
		sleep(.5)
		csvoutput=[]
		csvoutput.extend((time(), sensor_value, voltage,R0,RS,ppm,sound_value))
		write_csv(csvoutput)

	except IOError:
   		print ("Error")
