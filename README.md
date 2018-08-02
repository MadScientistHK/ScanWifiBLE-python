# ScanWifiBLE-python


Use only the files in Ultra Robuste

type the following commands :

all in one : 

```sh 
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install git -y && sudo apt-get install libusb-dev -y && sudo apt-get install libglib2.0-dev --fix-missing -y && sudo apt-get install libudev-dev -y &sudo apt-get install git& sudo apt-get install libical-dev -y && sudo apt-get install libreadline-dev -y && sudo apt-get install libdbus-glib-1-dev -y && sudo apt-get install bluetooth bluez blueman -y && sudo apt-get install python-bluez -y && sudo apt-get install python-pip -y && sudo pip install wifi && sudo pip install paho-mqtt
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
sudo apt-get install git -y
sudo git clone https://github.com/oblique/create_ap.git
sudo cd create_ap
sudo make install
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

create_ap -n wlan0 MyAccessPoint MyPassPhrase


$ sudo apt-get install git lighttpd php7.0-cgi hostapd dnsmasq














































































(chmod +x /etc/NetworkManager/dispatcher.d/freewifi.sh)
