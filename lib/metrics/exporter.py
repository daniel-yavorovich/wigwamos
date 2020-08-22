from prometheus_client import Gauge, Info

GROW_INFO = Info('growing', 'Grow info')
AIR_TEMPERATURE = Gauge('air_temperature', 'Air temperature')
AIR_HUMIDITY = Gauge('air_humidity', 'Air humidity')
SOIL_MOISTURE = Gauge('soil_moisture', 'Soil moisture')
WATER_LEVEL = Gauge('water_level', 'Water level')
PI_TEMPERATURE = Gauge('pi_temperature', 'Raspberry PI CPU temperature')
LIGHT_BRIGHTNESS = Gauge('light_brightness', 'Light brightness')
FAN_SPEED = Gauge('fan_speed', 'Fan speed')
TARGET_TEMPERATURE = Gauge('target_temperature', 'Target temperature')
TARGET_HUMIDITY = Gauge('target_humidity', 'Target humidity')
HUMIDIFIER_PUMP_USAGE = Gauge('humidifier_pump_usage', 'Humidifier pump usage')
