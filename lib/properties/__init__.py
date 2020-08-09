from .models import Property as PropertyModel


class Property:
    def __init__(self):
        pass

    def set_property(self, key, value):
        item = self.get_property_value(key)
        if item:
            PropertyModel.update({PropertyModel.value: value}).where(PropertyModel.key == key).execute()
        else:
            item = PropertyModel.create(key=key, value=value).save()

        return item

    def get_property_value(self, key):
        try:
            result = PropertyModel.get(PropertyModel.key == key)
        except PropertyModel.DoesNotExist:
            return None

        return result.value

    def delete_property(self, key):
        return PropertyModel.delete().where(PropertyModel.key == key).execute()
