
from types.stack_items import StackItems


class ByteArrayItem(StackItems):

    def __init__(self, val: bytearray):
        self.value = val

    def get_bytearray(self):
        return self.value