# RaspberryPI prepare
## Install depends
    sudo apt-get install python3-dev python3-pip
    sudo python3 -m pip install --upgrade pip setuptools wheel

## Enable I2C

    sudo raspi-config

on the command line, then use the arrow keys to select 'Interfacing Options' and 'I2C' to tell the RasPi to enable the I2C interface. Then select 'Finish' and reboot the RasPi.

