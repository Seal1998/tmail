#!/bin/bash
git pull
if [ $? -ne 0 ]; then
    echo "[*]Error while pulling new version from github. Exiting..."
    exit
fi

if [ $(diff ./tmail.py /usr/local/bin/tmail -q) = '' ]; then
    echo "[*]Nothing to update. Exiting..."
    exit

else
    echo "[*]Removing old /usr/local/bin/tmail"
    sudo rm /usr/local/bin/tmail
    ./install.sh
