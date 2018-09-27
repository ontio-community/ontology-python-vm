from types.stack_items import StackItems


class BoolItem(StackItems):

    def __init__(self, val: bool):
        self.value = val

    def get_biginteger(self):
        if self.value:
            return 1
        else:
            return 0

    def get_bool(self):
        return self.value

    def get_bytearray(self):
        if self.value:
            return bytearray(1)
        return bytearray(0)
