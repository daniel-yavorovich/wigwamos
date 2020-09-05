# WigwamOS

Software & install documentation for WigwamBox - Open Source smart growbox. 

[Install documentation](./INSTALL.md)

## Functions

* temperature control
  + if temperature is extreme high, system will temporary turn-off light
  + if temperature is extreme low, system will temporary turn-off humidify
* humidity control
* growing config management
* control light (day/night)
* water level control
* storage and display metrics graphs
* monitoring metrics & alerts into telegram channel
* display stats on micro display by button click

### Supported Metrics

* Temperature
* Humidity
* Grow days
* Water level
* PI CPU temperature
* Light brightness
* Fan speed
* Humidify water level

#### Grafana Dashboard screenshot

![grafana dashboard](./data/screenshots/grafana-dashboard.png)

## TODO
* LED dimmer for sunrise/sunset
* add button for show stats on display