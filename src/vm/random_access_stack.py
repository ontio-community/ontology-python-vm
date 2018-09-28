from src.types.array_item import ArrayItem
from src.types.bool_item import BoolItem
from src.types.bytearray_item import ByteArrayItem
from src.types.integer_item import IntegerItem
from src.types.stack_items import StackItems


class RandomAccessStack(object):
    def __init__(self):
        self.e = list()

    def info(self):
        info = "["
        for i in range(len(self.e)):
            class_name = self.e.__getitem__(i).__class__.__name__
            class_name.replace('Item', '')
            info = info + class_name
            if i != len(self.e) - 1:
                info = info + ","
        return info + "]"

    def info2(self):
        info = "["
        for i in range(len(self.e)):
            class_name = self.e.__getitem__(i).__class__.__name__
            class_name.replace('Item', '')
            if type(self.e[i]) == ByteArrayItem:
                class_name = class_name + "(" + self.e[i].get_bytearray().hex() + ")"
            elif type(self.e[i]) == IntegerItem:
                class_name = class_name + "(" + self.e[i].get_biginteger() + ")"
            elif type(self.e[i]) == BoolItem:
                class_name = class_name + "(" + self.e[i].get_bool() + ")"
            elif type(self.e[i]) == ArrayItem:
                arr = self.e[i].stack_items
                class_name = class_name + "["
                for j in range(len(arr)):
                    if type(arr[j]) == ByteArrayItem:
                        class_name = class_name + "ByteArray:" + arr[j].get_bytearray().hex()
                    elif type(arr[j]) == IntegerItem:
                        class_name = class_name + "Integer:" + arr[j].get_biginteger()
                    elif type(arr[j]) == BoolItem:
                        class_name = class_name + "Bool:" + arr[j].get_bool()
                    elif type(arr[j]) == ArrayItem:
                        class_name = class_name + "ArrayItem"
                    if j < len(arr) - 1:
                        class_name = class_name + ","
                class_name = class_name + "]"
            info = info + class_name
            if i != len(self.e) - 1:
                info = info + ","
        return info + "]"

    def count(self):
        return len(self.e)

    def insert(self, index: int, t: StackItems):
        if t == None:
            return
        index = len(self.e) - index
        self.e.insert(index, t)

    def peek(self, index: int):
        l = len(self.e)
        if index >= l:
            return None
        index = l- index
        return self.e[index -1]

    def remove(self, index: int):
        if index > len(self.e):
            return None
        index = len(self.e) - index
        return self.e.pop(index - 1)

    def set(self, index: int, t: StackItems):
        self.e.insert(index, t)

    def push(self, t: StackItems, index=0):
        self.insert(index, t)

    def pop(self):
        return self.remove(0)

    def swap(self, i: int, j: int):
        tmp = self.e[i]
        self.e.__setitem__(i, self.e[j])
        self.e.__setitem__(j, tmp)

    def copy_to(self, stack):
        stack.e.extend(self.e)













