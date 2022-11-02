#!/bin/bash

# Resolve HOST IP as syslog.host.
serverAddress="$(ip route | grep default | grep -oP '(?<=via\ ).*(?=\ dev)')"
tmpFile=`mktemp`

# Avoid "Device or resource busy" error on /etc/hosts
sed '/syslog.host/d' /etc/hosts > $tmpFile
echo "$serverAddress    syslog.host" >> $tmpFile
cat $tmpFile > /etc/hosts
rm -f $tmpFile

exit 0
