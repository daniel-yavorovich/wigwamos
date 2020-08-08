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
    
    sudo apt-get install python3-dev python3-pip libopenjp2-7 libtiff5 libleveldb-dev
    sudo python3 -m pip install --upgrade pip setuptools wheel

## Enable I2C

    sudo raspi-config


# Monitoring

    sudo apt-get install -y adduser libfontconfig1 prometheus
    
    cd /tmp
    wget https://dl.grafana.com/oss/release/grafana_7.1.3_armhf.deb
    sudo dpkg -i grafana_7.1.3_armhf.deb
    
    sudo /bin/systemctl daemon-reload
    sudo /bin/systemctl enable grafana-server
    sudo /bin/systemctl start grafana-server
    
    cp /etc/prometheus/prometheus.yml /etc/prometheus/prometheus.yml.orig
    tee -a /etc/prometheus/prometheus.yml << EOF
    
      - job_name: wigwamos
        scrape_interval: 5s
        scrape_timeout: 5s
        static_configs:
          - targets: ['localhost:8000']
    EOF
    systemctl restart prometheus.service