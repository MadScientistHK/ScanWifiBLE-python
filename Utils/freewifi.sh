#!/bin/sh

[ ! -f /sbin/iwconfig -o ! -x /sbin/iwconfig ] && exit 0
[ `/sbin/iwconfig 2>&1|grep -i freewifi|wc -l` -eq 0 ] && logger "Ce n'est pas FreeWifi ..." && exit 0

. /etc/freewifi.conf

wget -O - --post-data="login=$LOGIN&password=$PASSWORD" "https://wifi.free.fr/Auth" 2>/dev/null|grep "CONNEXION AU SERVICE REUSSIE" 1>/dev/null 2>&1 && logger "Connection FreeWifi OK" && exit 0
logger "Erreur de connection FreeWifi"
exit 0
