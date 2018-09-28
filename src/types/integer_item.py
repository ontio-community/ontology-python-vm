
from ontology import utils
from src.types.stack_items import StackItems


class IntegerItem(StackItems):
    def __init__(self, val: int):
        self.value = val

    def get_bytearray(self):
        return utils(self.value)

    def get_biginteger(self):
        return self.value