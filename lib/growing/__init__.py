import datetime
from ..properties import Property


class Growing(Property):
    START_GROWING_PROPERTY_KEY = 'start_growing_timestamp'

    def reset_day_counter(self):
        return self.set_property(self.START_GROWING_PROPERTY_KEY, str(datetime.datetime.now().timestamp()))

    def get_start_growing_date(self):
        start_timestamp = self.get_property_value(self.START_GROWING_PROPERTY_KEY)
        if not start_timestamp:
            self.reset_day_counter()
            start_timestamp = self.get_property_value(self.START_GROWING_PROPERTY_KEY)

        return datetime.datetime.fromtimestamp(float(self.get_property_value(self.START_GROWING_PROPERTY_KEY)))

    def get_growing_day_count(self):
        return (datetime.datetime.now() - self.get_start_growing_date()).days

    @property
    def is_day(self):
        # TODO: need implement
        return True
