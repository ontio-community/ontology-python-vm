from types.stack_items import StackItems


class StructItem(StackItems):
    def __init__(self, stack_items: list()):
        self.stack_items = stack_items

    def equals(self, other):
        if type(other) != StructItem:
            return False
        for i in range(len(self.stack_items)):
            if not self.stack_items[i].equals(other.stack_items[i]):
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
        return self.stack_items

    def get_map(self):
        return None

    def add(self, items: StackItems):
        self.stack_items.append(items)

    def count(self):
        return len(self.stack_items)


