from enum import Enum

from ontology.common.error_code import ErrorCode


class VMState(Enum):
    NONE = 0x00
    HALT = 0x01
    FAULT = 0x02
    BREAK = 0x04
    INSUFFICIENT_RESOURCE = 0x10

    def __init__(self, b: int):
        self.v = b

    def get_v(self):
        return self.v

    @staticmethod
    def value_of(b: int):
        for item in VMState.__members__.values():
            if item.value == b:
                return item
        raise Exception(ErrorCode.param_error)

