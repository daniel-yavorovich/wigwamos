import os

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LEVELDB_PATH = os.environ.get('LEVELDB_PATH', '/var/lib/wigwamos/')
EXPORTER_SERVER_PORT = int(os.environ.get('EXPORTER_SERVER_PORT', 8000))
EXPORTER_UPDATE_INTERVAL = int(os.environ.get('EXPORTER_UPDATE_INTERVAL', 10))

BOTTLE_HEIGHT = float(os.environ.get('BOTTLE_HEIGHT', 23.6))
