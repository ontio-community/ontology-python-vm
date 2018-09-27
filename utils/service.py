from ontology.common.address import Address
from ontology.io.binary_writer import BinaryWriter
from ontology.io.memory_stream import StreamManager
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from types.array_item import ArrayItem
from types.bool_item import BoolItem
from types.bytearray_item import ByteArrayItem
from types.integer_item import IntegerItem
from types.interop_item import InteropItem
from types.map_item import MapItem
from types.stack_items import StackItems
from types.struct_item import StructItem
from utils.config import Config
from utils.push_data import PushData
from utils.vm_reader import VmReader
from vm.execution_engine import ExecutionEngine


class Service(object):
    def __init__(self, exec_method = None, validator_method = None):
        self.exec_func = exec_method
        self.validator_method = validator_method

    def exec(self, config: Config, engine: ExecutionEngine):
        try:
            self.exec_func(config, engine)
        except Exception as e:
            raise e

    def storage_put(self, config: Config, engine: ExecutionEngine):
        item = PushData.pop_interop_interface(engine)
        key = PushData.pop_bytearray(engine)
        value = PushData.pop_bytearray(engine)
        config.get_storage_map()[item.value.decode('utf-8') + key.decode('utf-8')] = value

    def storage_get_context(self, config: Config, engine: ExecutionEngine):
        PushData.push_data(engine, InteropItem(config.contract_address.encode('utf-8')))

    def storage_get(self, config: Config, engine: ExecutionEngine):
        item = PushData.pop_interop_interface(engine)
        key = PushData.pop_bytearray(engine)
        value = config.get_storage_map()[item.value.decode('utf-8') + key.decode('utf-8')]
        if value is None:
            value = bytearray()
        PushData.push_data(engine, value)

    def runtime_log(self, config: Config, engine: ExecutionEngine):
        item = PushData.pop_bytearray(engine)
        print("Runtimelog:", item.decode('utf-8'))

    def runtime_notify(self, config: Config, engine: ExecutionEngine):
        item = PushData.pop_stack_item(engine)
        print("RuntimeNotify:", self.__convert_neovm_type_hex_str(item))

    def runtime_check_witness(self, config: Config, engine: ExecutionEngine):
        data = PushData.pop_bytearray(engine)
        if len(data) == 20:
            address = Address(data)
            l = config.get_signature_addresses()
            if address.b58encode() in l:
                PushData.push_data(engine, BoolItem(True))
            else:
                PushData.push_data(engine, BoolItem(False))

    def runtime_deserialize(self, config: Config, engine: ExecutionEngine):
        bys = PushData.pop_bytearray(engine)
        reader = VmReader(bys)
        items = self.__deserialize_stack_item(reader)
        PushData.push_data(engine, items)

    def runtime_serialize(self, config: Config, engine: ExecutionEngine):
        t = PushData.pop_stack_item(engine)
        writer = BinaryWriter(StreamManager.GetStream())
        baos = self.__serialize_stack_item(t, writer)
        PushData.push_data(engine, baos.stream.ToArray())

    def __serialize_stack_item(self, item: StackItems, writer: BinaryWriter):
        if type(item) == ByteArrayItem:
            writer.write_byte(BuildParams.Type.bytearraytype.value)
            bys = item.get_bytearray()
            writer.write_var_bytes(bys)
        elif type(item) == IntegerItem:
            writer.write_byte(BuildParams.Type.integertype.value)
            bys = item.get_bytearray()
            writer.write_var_bytes(bys)
        elif type(item) == BoolItem:
            writer.write_byte(BuildParams.Type.booltype.value)
            bys = item.get_bytearray()
            writer.write_var_bytes(bys)
        elif type(item) == ArrayItem:
            writer.write_byte(BuildParams.Type.arraytype.value)
            arr = item.get_array()
            writer.write_var_int(len(arr))
            for i in range(len(arr)):
                self.__serialize_stack_item(item, writer)
        elif type(item) == StructItem:
            pass
        elif type(item) == MapItem:
            writer.write_byte(BuildParams.Type.maptype.value)
            map = item.get_map()
            writer.write_var_int(len(map))
            for key, value in map.items():
                self.__serialize_stack_item(key, writer)
                self.__serialize_stack_item(value, writer)
        else:
            pass

    def __deserialize_stack_item(self, reader: VmReader):
        bt = reader.read_byte()
        if bt == BuildParams.Type.bytearraytype.value:
            val = reader.read_var_bytes()
            return ByteArrayItem(val)
        elif bt == BuildParams.Type.booltype.value:
            return BoolItem(reader.read_bool())
        elif bt == BuildParams.Type.integertype:
            b = int.from_bytes(reader.read_var_bytes())
            return IntegerItem(b)
        elif bt == BuildParams.Type.arraytype.value:
            count = reader.read_var_int()
            arr = list()
            for i in range(count):
                arr[i] = self.__deserialize_stack_item(reader)
            return ArrayItem(arr)
        elif bt == BuildParams.Type.structtype.value:
            count = reader.read_var_int()
            arr = list()
            for i in range(count):
                arr[i] = self.__deserialize_stack_item(reader)
            return StructItem(arr)
        elif bt == BuildParams.Type.maptype.value:
            count = reader.read_var_int()
            map = MapItem()
            for i in range(count):
                key = self.__deserialize_stack_item(reader)
                value = self.__deserialize_stack_item(reader)
                map.map[key] = value
            return map
        return None

    def __convert_neovm_type_hex_str(self, item: StackItems):
        if item is None:
            return None
        if type(item) == ByteArrayItem:
            bys = item.get_bytearray()
            return bys.hex()
        elif type(item) == IntegerItem:
            return item.get_biginteger()
        elif type(item) == BoolItem:
            return item.get_bool()
        elif type(item) == ArrayItem:
            l = list()
            for i in range(len(item.get_array())):
                obj = self.__convert_neovm_type_hex_str(item.get_array()[i])
                l.append(obj)
            l.__setitem__(0, l[0] + "(" + l[0] + ")")
            return l
        elif type(item) == StructItem:
            pass
        elif type(item) == InteropItem:
            return item.get_bytearray().hex()
        else:
            return None
        return None





