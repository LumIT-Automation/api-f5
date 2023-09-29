#!/bin/bash

apt update
apt install -y apt-utils ca-certificates gnupg
apt install -y procps net-tools dnsutils wget curl nano

mv /hashicorp-archive-keyring.gpg /etc/apt/trusted.gpg.d/
mv /hashicorp.list /etc/apt/sources.list.d/

apt update
apt install -y /*.deb
rm -f /*.deb

exit 0
