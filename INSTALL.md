# RaspberryPI prepare
After write image:

    cd /Volumes/boot
    touch ssh
    tee wpa_supplicant.conf << EOF
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    network={
        ssid="soul_wlan_travel_2G"
        psk="88888888"
        key_mgmt=WPA-PSK
    }
    EOF

After first boot please configure:

* Reset password
* Hostname
* Network
* SSH enable

## Install depends
    sudo apt-get install python3-dev python3-pip libopenjp2-7 libtiff5
    sudo python3 -m pip install --upgrade pip setuptools wheel

## Enable I2C

    sudo raspi-config

## Configure UART

https://www.raspberrypi.org/documentation/configuration/uart.md


on the command line, then use the arrow keys to select 'Interfacing Options' and 'I2C' to tell the RasPi to enable the I2C interface. Then select 'Finish' and reboot the RasPi.

## Install WiringPi libs

    sudo apt-get install wiringpi

    #For Pi 4, you need to update it：
    cd /tmp
    wget https://project-downloads.drogon.net/wiringpi-latest.deb
    sudo dpkg -i wiringpi-latest.deb
    gpio -v
    #You will get 2.52 information if you install it correctly