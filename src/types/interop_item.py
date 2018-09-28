from src.types.stack_items import StackItems


class InteropItem(StackItems):
    def __init__(self, val: bytearray):
        self.value = val

    def get_interface(self):
        return self