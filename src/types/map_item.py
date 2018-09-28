from src.types.bytearray_item import ByteArrayItem
from src.types.integer_item import IntegerItem
from src.types.stack_items import StackItems


class MapItem(StackItems):
    def __init__(self):
        self.map = dict()

    def add(self, key: StackItems, value: StackItems):
        self.map[key] = value

    def clear(self):
        self.map.clear()

    def contains_key(self, item: StackItems):
        return self.map.__contains__(item)

    def remove(self, item: StackItems):
        self.map.__delitem__(item)

    def equals(self, other: StackItems):
        for key, value in self.map.items():
            try:
                v = other.map[key]
                if v != value:
                    return False
            except Exception:
                return False
        return True

    def get_biginteger(self):
        return None

    def get_bool(self):
        return True

    def get_bytearray(self):
        return None

    def get_interface(self):
        return None

    def get_array(self):
        return None

    def get_struct(self):
        return None

    def get_map(self):
        return self.map

    def try_get_value(self, key: StackItems):
        for k, v in self.map.items():
            if type(k) == ByteArrayItem:
                if type(key) == ByteArrayItem:
                    if k.value.hex() == key.value.hex():
                        return v
                elif type(key) == IntegerItem:
                    if k.get_biginteger() == key.get_biginteger():
                        return v
        return None


