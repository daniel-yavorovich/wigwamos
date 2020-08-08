import plyvel
from settings import LEVELDB_PATH


class Property:
    def __init__(self):
        self.db = plyvel.DB(LEVELDB_PATH, create_if_missing=True)

    def set_property(self, key, value):
        return self.db.put(key.encode('utf8'), value.encode('utf8'))

    def get_property_value(self, key):
        result = self.db.get(key.encode('utf8'))
        if result:
            return result.decode('utf8')
        return None
