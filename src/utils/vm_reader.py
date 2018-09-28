from ontology.io.binary_reader import BinaryReader
from ontology.io.memory_stream import StreamManager


class VmReader(object):
    def __init__(self, bys: bytearray):
        self.ms = StreamManager.GetStream(bys)
        self.reader = BinaryReader(self.ms)
        self.code = bys

    def read_byte(self):
        return self.reader.read_byte()

    def read_bool(self):
        b = self.reader.read_byte()
        return b == 1

    def read_bytes(self, count: int):
        return self.reader.read_bytes(count)

    def read_var_bytes(self):
        return self.reader.read_var_bytes()

    def read_uint16(self):
        return self.read_uint16()

    def read_uint32(self):
        return self.reader.read_int32()

    def read_uint64(self):
        return self.reader.read_int64()

    def position(self):
        return self.reader.stream.tell()

    def read_int16(self):
        try:
            res = bytearray(self.reader.read_bytes(2))
            res.reverse()
            return int(res.hex(), 16)
        except Exception as e:
            return 0

    def read_var_int(self):
        return self.reader.read_var_int()

    def seek(self, offset: int):
        return self.reader.stream.seek(offset)

