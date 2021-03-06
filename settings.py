import os

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
DATABASE = os.environ.get('DATABASE', 'sqlite:///wigwamos.db')
EXPORTER_SERVER_PORT = int(os.environ.get('EXPORTER_SERVER_PORT', 8000))
EXPORTER_UPDATE_INTERVAL = int(os.environ.get('EXPORTER_UPDATE_INTERVAL', 1))
RUN_INTERVAL = int(os.environ.get('RUN_INTERVAL', 1))
LIGHT_CONTROL_INTERVAL = int(os.environ.get('LIGHT_CONTROL_INTERVAL', 60))
FAN_CONTROL_INTERVAL = int(os.environ.get('FAN_CONTROL_INTERVAL', 60))
HUMIDIFY_CONTROL_INTERVAL = int(os.environ.get('HUMIDIFY_CONTROL_INTERVAL', 1))

UPDATE_WEATHER_INFO_INTERVAL = int(os.environ.get('UPDATE_WEATHER_INFO_INTERVAL', 0))
UPDATE_PHOTO_INTERVAL = int(os.environ.get('UPDATE_PHOTO_INTERVAL', 0))

BOTTLE_HEIGHT = float(os.environ.get('BOTTLE_HEIGHT', 20))

API_HOST = os.environ.get('API_HOST', '0.0.0.0')
API_PORT = int(os.environ.get('API_PORT', 80))
API_DEBUG = int(os.environ.get('API_DEBUG', 1))

OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY', 'changeme')
OPENWEATHERMAP_LOCATION = os.environ.get('OPENWEATHERMAP_LOCATION', 'California,US')

PHOTOS_DIR = os.environ.get('PHOTOS_DIR', '/data/photos')
