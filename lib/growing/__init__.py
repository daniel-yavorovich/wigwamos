from ..properties import Property


class Growing(Property):
    DAY_COUNT = 'day_count'

    def get_day_count(self):
        return int(self.get_property_value(self.DAY_COUNT))

    def reset_day_counter(self):
        return self.set_property(self.DAY_COUNT, 1)

    @property
    def is_day(self):
        # TODO: need implement
        return True
