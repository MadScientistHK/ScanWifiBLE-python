# ScanWifiBLE-python

Only use the files in the Just_this_files folder

type the following commands :

```sh
❯ sudo apt-get update -y && sudo apt-get -y upgrade
❯sudo apt-get install libusb-dev -y
❯sudo apt-get install libglib2.0-dev --fix-missing
❯sudo apt-get install libudev-dev -y
❯sudo apt-get install libical-dev -y 
❯sudo apt-get install libreadline-dev -y
❯sudo apt-get install libdbus-glib-1-dev -y 
❯sudo apt-get install bluetooth bluez blueman -y
❯sudo apt-get install python-bluez -y
❯sudo apt-get install python-pip
❯sudo pip install wifi
❯sudo mv app.service /lib/systemd/system/
❯sudo systemctl enable app.service
```
To disable auto start :
```sh
❯sudo systemctl disable app.service
```



(chmod +x /etc/NetworkManager/dispatcher.d/freewifi.sh)
