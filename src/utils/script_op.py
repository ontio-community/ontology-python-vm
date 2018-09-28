from enum import Enum


class ScriptOp(Enum):
    # Constants
    OP_PUSH0 = 0x00
    OP_PUSHF = OP_PUSH0
    OP_PUSHBYTES1 = 0x01
    OP_PUSHBYTES75 = 0x4B
    OP_PUSHDATA1= 0x4C
    OP_PUSHDATA2 = 0x4D
    OP_PUSHDATA4 = 0x4E
    OP_PUSHM1 = 0x4F
    OP_RESERVED = 0x50
    OP_PUSH1= 0x51
    OP_PUSHT = OP_PUSH1
    OP_PUSH2 = 0x52
    OP_PUSH3 = 0x53
    OP_PUSH4 = 0x54
    OP_PUSH5 = 0x55
    OP_PUSH6 = 0x56
    OP_PUSH7 = 0x57
    OP_PUSH8 = 0x58
    OP_PUSH9 = 0x59
    OP_PUSH10 = 0x5A
    OP_PUSH11 = 0x5B
    OP_PUSH12 = 0x5C
    OP_PUSH13 = 0x5D
    OP_PUSH14 = 0x5E
    OP_PUSH15 = 0x5F
    OP_PUSH16 = 0x60
    # Flowcontrol
    OP_NOP = 0x61
    OP_JMP = 0x62
    OP_JMPIF = 0x63
    OP_JMPIFNOT = 0x64
    OP_CALL = 0x65
    OP_RET = 0x66
    OP_APPCALL = 0x67
    OP_SYSCALL = 0x68
    OP_VERIFY = 0x69
    # stack
    OP_DUPFROMALTSTACK = 0x6A
    OP_TOALTSTACK = 0x6B
    OP_FROMALTSTACK = 0x6C
    OP_XDROP = 0x6D
    OP_XSWAP = 0x72
    OP_XTUCK = 0x73
    OP_DEPTH = 0x74
    OP_DROP = 0x75
    OP_DUP = 0x76
    OP_NIP = 0x77
    OP_OVER = 0x78
    OP_PICK = 0x79
    OP_ROLL = 0x7A
    OP_ROT = 0x7B
    OP_SWAP = 0x7C
    OP_TUCK = 0x7D
     # Splice
    OP_CAT = 0x7E
    OP_SUBSTR = 0x7F
    OP_LEFT = 0x80
    OP_RIGHT = 0x81
    OP_SIZE = 0x82

     # Bitwise logic
    OP_INVERT = 0x83
    OP_AND = 0x84
    OP_OR = 0x85
    OP_XOR = 0x86
    OP_EQUAL = 0x87

     # Arithmetic
    OP_INC = 0x8B
    OP_DEC = 0x8C
    OP_SIGN = 0x8D
    OP_NEGATE = 0x8F
    OP_ABS = 0x90
    OP_NOT = 0x91
    OP_NZ = 0x92
    OP_ADD = 0x93
    OP_SUB = 0x94
    OP_MUL = 0x95
    OP_DIV = 0x96
    OP_MOD = 0x97
    OP_SHL = 0x98
    OP_SHR = 0x99
    OP_BOOLAND = 0x9A
    OP_BOOLOR = 0x9B
    OP_NUMEQUAL = 0x9C
    OP_NUMNOTEQUAL = 0x9E
    OP_LT = 0x9F
    OP_GT = 0xA0
    OP_LTE = 0xA1
    OP_GTE = 0xA2
    OP_MIN = 0xA3
    OP_MAX = 0xA4
    OP_WITHIN  = 0xA5

    # Crypto
    OP_SHA1 = 0xA7
    OP_SHA256 = 0xA8
    OP_HASH160 = 0xA9
    OP_HASH256 = 0xAA
    OP_CHECKSIG = 0xAC
    # OP_VERIFY = 0xAD
    OP_CHECKMULTISIG = 0xAE

    # Array
    OP_ARRAYSIZE = 0xC0
    OP_PACK = 0xC1
    OP_UNPACK = 0xC2
    OP_PICKITEM = 0xC3
    OP_SETITEM = 0xC4
    OP_NEWARRAY = 0xC5
    OP_NEWSTRUCT = 0xC6
    OP_NEWMAP = 0xC7
    OP_APPEND = 0xC8
    OP_REVERSE = 0xC9
    OP_REMOVE = 0xCA
    OP_HASKEY = 0xCB
    OP_KEYS = 0xCC
    OP_VALUES = 0xCD

    # OP_ANY = 0xCE
    # OP_SUM = 0xCF
    # OP_AVERAGE = 0xD0
    # OP_MAXITEM = 0xD1
    # OP_MINITEM = 0xD2
    #
    OP_THROW = 0xF0
    OP_THROWIFNOT = 0xF1

    @staticmethod
    def value_of(v: int):
        for item in ScriptOp.__members__.values():
            if item.value == v:
                return item
        return None