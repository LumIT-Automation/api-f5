#!/bin/bash

apt update
apt install -y procps net-tools dnsutils wget curl nano

apt install -y /*.deb
rm -f /*.deb

exit 0
