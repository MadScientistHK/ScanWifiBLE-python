# -*- coding: utf-8 -*-
import wifi
from util import *

def Search():
    wifilist = []

    cells = wifi.Cell.all('wlan0')

    for cell in cells:
        wifilist.append(cell)
        #print( str(cell.ssid)+", " )
    return wifilist


def FindFromSearchList(ssid):
    wifilist = Search()

    for cell in wifilist:
        if cell.ssid == ssid:
            return cell

    return False


def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)

    if cell:
        return cell

    return False


def Connect(ssid, password=None):
    cell = FindFromSearchList(ssid)

    if cell:
        savedcell = FindFromSavedList(cell.ssid)

        # Already Saved from Setting
        if savedcell:
            savedcell.activate()
            return cell

        # First time to conenct
        else:
            if cell.encrypted:
                if password:
                    scheme = Add(cell, password)

                    try:
                        scheme.activate()

                    # Wrong Password
                    except wifi.exceptions.ConnectionError:
                        Delete(ssid)
                        return False

                    return cell
                else:
                    return False
            else:
                scheme = Add(cell)

                try:
                    scheme.activate()
                except wifi.exceptions.ConnectionError:
                    Delete(ssid)
                    return False

                return cell

    return False


def Add(cell, password=None):
    if not cell:
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme


def Delete(ssid):
    if not ssid:
        return False

    cell = FindFromSavedList(ssid)

    if cell:
        cell.delete()
        return True

    return False


def Search_open():
    wifilist = Search()
    wifiopenlist = []
    i=0
    for i in range(len(wifilist)):
        if wifilist[i].encrypted == False:
            wifiopenlist.append(str(wifilist[i].ssid))
    return wifiopenlist



if __name__ == '__main__':
    # Search WiFi and return WiFi list
    #print(Search())
    # Connect WiFi with password & without password
    #print(Connect('OpenWiFi'))
    #print(Search_open())
    try:
        while 1:
	    #print 'before checkinternet'
            while checkInternet() == False:
		#print 'after checkinternet'
		result = Search_open()
		print "before open file"
		f = open('logOpen.txt','a')
		print "after open file"
                for i in range(len(result)):
		    print "before writing file"
		    f.write('try to connect to : '+str(result)+'\n')
                    Connect(result[i])
                    if checkInternet() == True:
			f.write('success to connect to : '+str(result)+'\n')
                        break
	    	f.close()
    except:print "Failed"
