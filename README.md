# ScanWifiBLE-python

Only use the files in the Just_this_files folder

type the following commands :

all in one : 

```sh 
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install libusb-dev -y && sudo apt-get install libglib2.0-dev --fix-missing -y && sudo apt-get install libudev-dev -y && sudo apt-get install libical-dev -y && sudo apt-get install libreadline-dev -y && sudo apt-get install libdbus-glib-1-dev -y && sudo apt-get install bluetooth bluez blueman -y && sudo apt-get install python-bluez -y && sudo apt-get install python-pip -y && sudo pip install wifi && sudo pip install paho-mqtt -y
```

```sh
sudo apt-get update -y && sudo apt-get upgrade -y 
sudo apt-get install libusb-dev -y 
sudo apt-get install libglib2.0-dev --fix-missing -y 
sudo apt-get install libudev-dev -y 
sudo apt-get install libical-dev -y 
sudo apt-get install libreadline-dev -y 
sudo apt-get install libdbus-glib-1-dev -y 
sudo apt-get install bluetooth bluez blueman -y 
sudo apt-get install python-bluez -y 
sudo apt-get install python-pip -y 
sudo pip install wifi 
sudo pip install paho-mqtt -y

sudo mv app.service /lib/systemd/system/
sudo systemctl enable app.service
```
To disable auto start :
```sh
❯sudo systemctl disable app.service
```



(chmod +x /etc/NetworkManager/dispatcher.d/freewifi.sh)
