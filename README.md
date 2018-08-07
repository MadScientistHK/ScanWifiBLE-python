# ScanWifiBLE-python


type the following commands :

all in one : 

```sh 
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install git -y && sudo apt-get install libusb-dev -y && sudo apt-get install libglib2.0-dev --fix-missing -y && sudo apt-get install libudev-dev -y &sudo apt-get install git& sudo apt-get install libical-dev -y && sudo apt-get install libreadline-dev -y && sudo apt-get install libdbus-glib-1-dev -y && sudo apt-get install bluetooth bluez blueman -y && sudo apt-get install python-bluez -y && sudo apt-get install python-pip -y && sudo pip install wifi && sudo pip install paho-mqtt && sudo reboot now
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

Fake AP (use c.py and don't forget to create the file address.txt)

```sh
sudo apt-get install git lighttpd hostapd dnsmasq -y
sudo git clone https://github.com/oblique/create_ap.git
cd create_ap
sudo make install
cd ..
```
and to activate at boot :

```sh
sudo mv ap_counter.service /lib/systemd/system/
sudo systemctl enable ap_counter.service 
```
