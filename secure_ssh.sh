#!/bin/sh

if [ $1 == 'unsecure' ]; then
 sed -i 's/RSAAuthentication yes/RSAAuthentication no/' /etc/ssh/sshd_config
 sed -i 's/PubkeyAuthentication yes/PubkeyAuthentication no/' /etc/ssh/sshd_config
 sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
 sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config

elif [ $1 == 'secure' ]; then
 sed -i 's/RSAAuthentication no/RSAAuthentication yes/' /etc/ssh/sshd_config
 sed -i 's/PubkeyAuthentication no/PubkeyAuthentication yes/' /etc/ssh/sshd_config
 sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
 sed -i 's/PermitRootLogin yes/#PermitRootLogin yes/' /etc/ssh/sshd_config
fi