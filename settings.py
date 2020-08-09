import os

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
DATABASE = os.environ.get('DATABASE', 'sqlite:///wigwamos.db')
EXPORTER_SERVER_PORT = int(os.environ.get('EXPORTER_SERVER_PORT', 8000))
EXPORTER_UPDATE_INTERVAL = int(os.environ.get('EXPORTER_UPDATE_INTERVAL', 10))
RUN_INTERVAL = int(os.environ.get('RUN_INTERVAL', 5))
LIGHT_CONTROL_INTERVAL = int(os.environ.get('LIGHT_CONTROL_INTERVAL', 60))
FAN_CONTROL_INTERVAL = int(os.environ.get('FAN_CONTROL_INTERVAL', 10))

BOTTLE_HEIGHT = float(os.environ.get('BOTTLE_HEIGHT', 23.6))
