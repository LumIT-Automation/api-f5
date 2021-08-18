#!/bin/bash

# Resolve HOST IP as syslog.host.
serverAddress="$(ip route | grep default | grep -oP '(?<=via\ ).*(?=\ dev)')"

sed -i '/syslog.host/d' /etc/hosts
echo "$serverAddress        syslog.host" >> /etc/hosts

exit 0
