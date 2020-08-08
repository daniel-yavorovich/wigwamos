# Functions

## High level

Automatize grooving process

* temperature and humidity control
* understanding day of progress
* air humidity control
* soil moisture control
* water level control
* display stats on micro display
* storage temperature and humidity metrics

## Details

* control light
* control fan (https://xn----itbbja1ajgfecfvb9m.xn--p1ai/raznoe/optimalnaya-temperatura-v-groubokse-d-2kanna-biz-502-bad-gateway.html#i)

## Programs
* metrics storage: every 10 sec
* light control: every 1 min
    + on/off
* climate control: every 1 min
    + humidity
    + temperature
* soil_moisture control: every 10 min
* display stats on display: by hw button click

### Prometheus exporter
Get data from sensors/db for metrics:

* Temperature
* Humidity
* Soil moisture
* grow days
* Water level
* PI CPU temperature
* Light brightness
* Fan speed

### Light control
Control light, based on growing process

* On/off
* Brightness, based on sunrise/sunset

### Growing control

* Set start growing day
* Get growing day
* Get progress in %

