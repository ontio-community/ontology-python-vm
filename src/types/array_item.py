from src.types.stack_items import StackItems


class ArrayItem(StackItems):
    def __init__(self, items: list()):
        self.stack_items = items

    def get_array(self):
        return self.stack_items
