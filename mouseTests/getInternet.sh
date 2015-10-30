#! /bin/sh

route add default gw 192.168.7.1 usb0
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
sudo ntpdate -s time.nist.gov
echo done
