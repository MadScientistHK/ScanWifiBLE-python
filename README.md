# ScanWifiBLE-python

https://scribles.net/setting-up-serial-communication-between-raspberry-pi-and-pc/

Use only the files in Ultra Robuste

type the following commands :

all in one : 

```sh 
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install libusb-dev -y && sudo apt-get install libglib2.0-dev --fix-missing -y && sudo apt-get install libudev-dev -y && sudo apt-get install libical-dev -y && sudo apt-get install libreadline-dev -y && sudo apt-get install libdbus-glib-1-dev -y && sudo apt-get install bluetooth bluez blueman -y && sudo apt-get install python-bluez -y && sudo apt-get install python-pip -y && sudo pip install wifi && sudo pip install paho-mqtt
```

One by one :

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
sudo pip install paho-mqtt
```

To activate the scan at boot

```sh
sudo mv app.service /lib/systemd/system/
sudo systemctl enable app.service
```

To disable the scan at boot :

```sh
❯sudo systemctl disable app.service
```


















































































(chmod +x /etc/NetworkManager/dispatcher.d/freewifi.sh)
