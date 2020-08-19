# RaspberryPI prepare
After write image:

    cd /Volumes/boot
    touch ssh
    tee wpa_supplicant.conf << EOF
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    network={
        ssid="soul_wlan_2G"
        psk="0010100101"
        key_mgmt=WPA-PSK
    }
    EOF

After first boot please configure:

* Reset password
* Hostname
* Network
* Enable SSH
* Enable I2C

## Install depends
    
    sudo apt-get install python3-dev python3-pip libopenjp2-7 libtiff5 libleveldb-dev supervisor libatlas-base-dev
    sudo python3 -m pip install --upgrade pip setuptools wheel
    
## Monitoring

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
    
## Configure supervisor
    
    systemctl enable supervisor
    tee /etc/supervisor/conf.d/wigwamos.conf << EOF
    [program:wigwamos]
    command=/home/pi/wigwamos/run.py
    directory=/home/pi/wigwamos/
    autostart=true
    autorestart=true
    stdout_logfile=/var/log/wigwamos.log
    stderr_logfile=/var/log/wigwamos.log
    stdout_logfile_maxbytes=1MB
    stdout_logfile_backups=10
    stderr_logfile_maxbytes=1MB
    stderr_logfile_backups=10
    
    [program:api]
    command=/usr/local/bin/flask run -h 0.0.0.0
    directory=/home/pi/wigwamos/
    autostart=true
    autorestart=true
    environment=FLASK_APP="api.py"
    stdout_logfile=/var/log/wigwamos-api.log
    stderr_logfile=/var/log/wigwamos-api.log
    stdout_logfile_maxbytes=1MB
    stdout_logfile_backups=10
    stderr_logfile_maxbytes=1MB
    stderr_logfile_backups=10
    EOF
    systemctl reload supervisor

## Init database

    cd /home/pi/wigwamos/
    python init.py