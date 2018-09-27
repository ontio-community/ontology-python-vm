from ontology.crypto.digest import Digest
from types.array_item import ArrayItem
from types.bool_item import BoolItem
from types.bytearray_item import ByteArrayItem
from types.integer_item import IntegerItem
from types.interop_item import InteropItem
from types.map_item import MapItem
from types.stack_items import StackItems
from types.struct_item import StructItem
from utils.script_op import ScriptOp
from vm.vm_state import VMState


class PushData(object):
    @staticmethod
    def op_push_data(engine):
        data = PushData.get_push_data(engine)
        PushData.push_data(engine, data)
        return VMState.NONE

    @staticmethod
    def get_push_data(e):
        data = None
        if ScriptOp.OP_PUSHBYTES1.value <= e.op_code.value <= ScriptOp.OP_PUSHBYTES75.value:
            data = e.context.op_reader.read_bytes(e.op_code.value)
        if e.op_code == ScriptOp.OP_PUSH0:
            data = 0
        elif e.op_code == ScriptOp.OP_PUSHDATA1:
            b = e.context.op_reader.read_byte()
            data = e.context.op_reader.read_bytes(b)
        elif e.op_code == ScriptOp.OP_PUSHDATA2:
            data = e.context.op_reader.read_bytes(2)
        elif e.op_code == ScriptOp.OP_PUSHDATA4:
            data = e.context.op_reader.read_bytes(4)
        elif e.op_code == ScriptOp.OP_PUSH1 or ScriptOp.OP_PUSH1.value <= e.op_code.value <= ScriptOp.OP_PUSH16.value:
            data = e.op_code.value - ScriptOp.OP_PUSH1.value + 1
        return data

    @staticmethod
    def push_data(engine, data):
        if type(data) is int:
            engine.evaluation_stack.push(IntegerItem(data))
        elif type(data) is bool:
            engine.evaluation_stack.push(BoolItem(data))
        elif type(data) is bytearray or type(data) is bytes:
            engine.evaluation_stack.push(ByteArrayItem(data))
        elif type(data) is ArrayItem:
            engine.evaluation_stack.push(ArrayItem(data.stack_items))
        elif type(data) is IntegerItem:
            engine.evaluation_stack.push(data)
        elif type(data) is BoolItem:
            engine.evaluation_stack.push(data)
        elif type(data) is ByteArrayItem:
            engine.evaluation_stack.push(data)
        elif type(data) is MapItem:
            engine.evaluation_stack.push(data)
        elif type(data) is StructItem:
            engine.evaluation_stack.push(data)
        elif type(data) is StackItems:
            engine.evaluation_stack.push(data)
        elif type(data) is list:
            engine.evaluation_stack.push(ArrayItem(data))
        elif type(data) is InteropItem:
            engine.evaluation_stack.push(data)

    @staticmethod
    def op_nop(engine):
        return VMState.NONE

    @staticmethod
    def op_jmp(engine):
        offset = engine.context.op_reader.read_int16()
        offset = engine.context.get_instruction_pointer() + offset - 3
        if offset < 0 or offset > len(engine.context.code):
            return VMState.FAULT
        f_value = True
        if engine.op_code.value > ScriptOp.OP_JMP.value:
            if PushData.evaluation_stack_count(engine) < 1:
                return VMState.FAULT
            f_value = PushData.pop_bool(engine)
            if engine.op_code == ScriptOp.OP_JMPIFNOT:
                f_value = not f_value
        if f_value:
            engine.context.set_instruction_pointer(offset)
        return VMState.NONE

    @staticmethod
    def op_call(engine):
        execution_context = engine.context.clone()
        engine.context.set_instruction_pointer(engine.context.get_instruction_pointer() + 2)
        engine.op_code = ScriptOp.OP_JMP
        engine.push_context(execution_context)
        return PushData.op_jmp(engine)

    @staticmethod
    def op_ret(engine):
        engine.pop_context()
        return VMState.NONE

    @staticmethod
    def op_to_dup_from_alt_stack(engine):
        PushData.push(engine, engine.alt_stack.peek(0))
        return VMState.NONE

    @staticmethod
    def op_to_alt_stack(engine):
        engine.alt_stack.push(PushData.pop_stack_item(engine))
        return VMState.NONE

    @staticmethod
    def op_from_alt_stack(engine):
        items = engine.alt_stack.pop()
        PushData.push(engine, items)
        return VMState.NONE

    @staticmethod
    def op_x_drop(engine):
        n = PushData.pop_int(engine)
        engine.alt_stack.remove(n)
        return VMState.NONE

    @staticmethod
    def op_x_swap(engine):
        n = PushData.pop_int(engine)
        if n == 0:
            return VMState.NONE
        engine.evaluation_stack.swap(0, n)
        return VMState.NONE

    @staticmethod
    def op_x_tuck(engine):
        n = PushData.pop_int(engine)
        engine.evaluation_stack.insert(n, PushData.peek_stack_item(engine))
        return VMState.NONE

    @staticmethod
    def op_depth(engine):
        PushData.push_data(engine, PushData.count(engine))
        return VMState.NONE

    @staticmethod
    def op_drop(engine):
        PushData.pop_stack_item(engine)
        return VMState.NONE

    @staticmethod
    def op_dup(engine):
        items = PushData.peek_stack_item(engine)
        PushData.push(engine, items)
        return VMState.NONE

    @staticmethod
    def op_nip(engine):
        x2 = PushData.pop_stack_item(engine)
        PushData.peek_stack_item(engine)
        PushData.push(engine, x2)
        return VMState.NONE

    @staticmethod
    def op_over(engine):
        x2 = PushData.pop_stack_item(engine)
        x1 = PushData.peek_stack_item(engine)
        PushData.peek_stack_item(engine)
        PushData.push(engine, x2)
        PushData.push(engine, x1)
        return VMState.NONE

    @staticmethod
    def op_pick(engine):
        n = PushData.pop_int(engine)
        if n == 0:
            return VMState.NONE
        PushData.push(engine, engine.evaluation_stack.peek(n))
        return VMState.NONE

    @staticmethod
    def op_roll(engine):
        n = PushData.pop_int(engine)
        if n == 0:
            return VMState.NONE
        PushData.push(engine, engine.evaluation_stack.remove(n))
        return VMState.NONE

    @staticmethod
    def op_rot(engine):
        x3 = PushData.pop_stack_item(engine)
        x2 = PushData.pop_stack_item(engine)
        x1 = PushData.pop_stack_item(engine)
        PushData.push(engine, x2)
        PushData.push(engine, x3)
        PushData.push(engine, x1)
        return VMState.NONE

    @staticmethod
    def op_swap(engine):
        x2 = PushData.pop_stack_item(engine)
        x1 = PushData.pop_stack_item(engine)
        PushData.push(engine, x2)
        PushData.push(engine, x1)
        return VMState.NONE

    @staticmethod
    def op_tuck(engine):
        x2 = PushData.pop_stack_item(engine)
        x1 = PushData.pop_stack_item(engine)
        PushData.push(engine, x2)
        PushData.push(engine, x1)
        PushData.push(engine, x2)
        return VMState.NONE

    @staticmethod
    def concat(array1: bytearray, array2: bytearray):
        return array1 + array2

    @staticmethod
    def op_cat(engine):
        bs2 = PushData.pop_bytearray(engine)
        bs1 = PushData.pop_bytearray(engine)
        r = PushData.concat(bs1, bs2)
        PushData.push_data(engine, r)
        return VMState.NONE

    @staticmethod
    def op_sub_str(engine):
        count = PushData.pop_int(engine)
        index = PushData.pop_int(engine)
        arr = PushData.pop_bytearray(engine)
        bs = arr[index:index+count]
        PushData.push_data(engine, bs)
        return VMState.NONE

    @staticmethod
    def op_left(engine):
        count = PushData.pop_int(engine)
        arr = PushData.pop_bytearray(engine)
        bs = arr[0:count]
        PushData.push_data(engine, bs)
        return VMState.NONE

    @staticmethod
    def op_right(engine):
        count = PushData.pop_int(engine)
        arr = PushData.pop_bytearray(engine)
        bs = arr[len(arr)-count:]
        PushData.push_data(engine, bs)
        return VMState.NONE

    @staticmethod
    def op_size(engine):
        arr = PushData.pop_bytearray(engine)
        PushData.push_data(engine, len(arr))
        return VMState.NONE

    @staticmethod
    def op_invert(engine):
        i = PushData.pop_int()
        PushData.push_data(engine, i)
        return VMState.NONE

    @staticmethod
    def op_equal(engine):
        b1 = PushData.pop_stack_item(engine)
        b2 = PushData.pop_stack_item(engine)
        PushData.push_data(engine, b1.equals(b2))
        return VMState.NONE

    @staticmethod
    def op_array_size(engine):
        item = PushData.pop_stack_item(engine)
        if type(item) is ArrayItem:
            bys = item.get_array()
            PushData.push_data(engine, len(bys))
        else:
            bys = item.get_bytearray()
            PushData.push_data(engine, len(bys))
        return VMState.NONE

    @staticmethod
    def op_pack(engine):
        size = PushData.pop_int(engine)
        items = list()
        for i in range(size):
            items.append(PushData.pop_stack_item(engine))
        PushData.push_data(engine, items)
        return VMState.NONE

    @staticmethod
    def op_unpack(engine):
        items = PushData.pop_array(engine)
        l = len(items)
        for i in range(l - 1, -1, -1):
            PushData.push(engine, items[i])
        PushData.push_data(engine, l)
        return VMState.NONE

    @staticmethod
    def op_pick_item(engine):
        index = PushData.pop_stack_item(engine)
        items = PushData.pop_stack_item(engine)
        if type(items) is ArrayItem:
            i = index.get_biginteger()
            arr = items.get_array()
            PushData.push_data(engine, arr[i])
        elif type(items) is MapItem:
            t = items.try_get_value(index)
            PushData.push_data(engine, t)
        return VMState.NONE

    @staticmethod
    def op_set_item(engine):
        new_item = PushData.pop_stack_item(engine)
        index = PushData.pop_stack_item(engine)
        item = PushData.pop_stack_item(engine)
        if type(item) is ArrayItem:
            i = index.get_biginteger()
            items = item.get_array()
            items[i] = new_item
        elif type(item) is MapItem:
            item.add(index, new_item)
        elif type(item) is StructItem:
            i = index.get_biginteger()
            item.stack_items.set(i, new_item)
        return VMState.NONE

    @staticmethod
    def op_new_array(engine):
        count = PushData.pop_int(engine)
        items = list()
        for i in range(count):
            items.append(BoolItem(False))
        PushData.push_data(engine, ArrayItem(items))
        return VMState.NONE

    @staticmethod
    def op_new_struct(engine):
        return VMState.NONE

    @staticmethod
    def op_new_map(engine):
        PushData.push_data(engine, MapItem())
        return VMState.NONE

    @staticmethod
    def op_append(engine):
        new_item = PushData.pop_stack_item(engine)
        items = PushData.pop_stack_item(engine)
        # TODO
        return VMState.NONE

    @staticmethod
    def op_reverse(engine):
        items = PushData.pop_array(engine)
        # TODO
        return VMState.NONE

    @staticmethod
    def op_throw(engine):
        return VMState.FAULT

    @staticmethod
    def op_throw_if_not(engine):
        b = PushData.pop_bool(engine)
        if not b:
            return VMState.FAULT
        return VMState.NONE

    @staticmethod
    def op_hash(engine):
        x = PushData.pop_bytearray(engine)
        PushData.push_data(engine, PushData.hash(x, engine))
        return VMState.NONE

    @staticmethod
    def op_sign(engine):
        x = PushData.pop_int(engine)
        if x < 0:
            PushData.push_data(engine, -1)
        elif x > 0:
            PushData.push_data(engine, 1)
        else:
            PushData.push_data(engine, 0)
        return VMState.NONE

    @staticmethod
    def op_not(engine):
        x = PushData.pop_bool(engine)
        PushData.push_data(engine, not x)
        return VMState.NONE

    @staticmethod
    def op_nz(engine):
        x = PushData.pop_int(engine)
        PushData.push_data(engine, PushData.bigint_comp(x, engine.op_code))
        return VMState.NONE

    @staticmethod
    def op_bigint_zip(engine):
        x2 = PushData.pop_int(engine)
        x1 = PushData.pop_int(engine)
        b = PushData.bigint_zip(x2, x1, engine.op_code)
        PushData.push_data(engine, b)
        return VMState.NONE

    @staticmethod
    def op_bigint(engine):
        x = PushData.pop_int(engine)
        if x <0:
            PushData.push_data(engine, -1)
        elif x> 0:
            PushData.push_data(engine, 1)
        else:
            PushData.push_data(engine, 0)

        return VMState.NONE

    @staticmethod
    def op_bool_zip(engine):
        x2 = PushData.pop_bool(engine)
        x1 = PushData.pop_bool(engine)
        b = PushData.bool_zip(x2, x1, engine.op_code)
        PushData.push_data(engine, b)
        return VMState.NONE

    @staticmethod
    def bool_zip(a: bool, b: bool, op: ScriptOp):
        if op == ScriptOp.BOOLAND:
            return a and b
        if op == ScriptOp.BOOLOR:
            return a or b
        return False

    @staticmethod
    def op_bigint_comp(engine):
        print(engine.evaluation_stack.e[0].value)
        print(engine.evaluation_stack.e[1].value)
        x2 = PushData.pop_int(engine)
        x1 = PushData.pop_int(engine)
        b = PushData.bigint_multi_comp(x1, x2, engine.op_code)
        PushData.push_data(engine, b)
        return VMState.NONE

    @staticmethod
    def op_within(engine):
        b = PushData.pop_int(engine)
        a = PushData.pop_int(engine)
        c = PushData.pop_int(engine)
        PushData.push_data(engine, PushData.within_op(c, a, b))
        return VMState.NONE

    @staticmethod
    def within_op(a: int, b: int, c: int):
        b1 = PushData.bigint_multi_comp(a, b, ScriptOp.GTE)
        b2 = PushData.bigint_multi_comp(a, c, ScriptOp.GTE)
        return PushData.bool_zip(b1, b2, ScriptOp.BOOLOR)

    @staticmethod
    def bigint_multi_comp(a: int, b: int, op: ScriptOp):
        if op == ScriptOp.OP_NUMEQUAL:
            return PushData.compare_to(a, b) == 0
        elif op == ScriptOp.OP_NUMNOTEQUAL:
            return PushData.compare_to(a, b) != 0
        elif op == ScriptOp.OP_LT:
            return PushData.compare_to(a, b) < 0
        elif op == ScriptOp.OP_GT:
            return PushData.compare_to(a, b) > 0
        elif op == ScriptOp.OP_LTE:
            return PushData.compare_to(a, b) <= 0
        elif op == ScriptOp.OP_GTE:
            return PushData.compare_to(a, b) >= 0
        return False


    @staticmethod
    def bigint_zip(a: int, b: int, op: ScriptOp):
        if op == ScriptOp.AND:
            return a and b
        elif op == ScriptOp.OR:
            return a or b
        elif op == ScriptOp.XOR:
            return a ^ b
        elif op == ScriptOp.ADD:
            return a + b
        elif op == ScriptOp.SUB:
            return a - b
        elif op == ScriptOp.MUL:
            return a * b
        elif op == ScriptOp.DIV:
            return a / b
        elif op == ScriptOp.MOD:
            return a % b
        elif op == ScriptOp.SHL:
            return a << b
        elif op == ScriptOp.SHR:
            return a >> b
        elif op == ScriptOp.MIN:
            if a < b:
                return a
            else:
                return b
        elif op == ScriptOp.MAX:
            if a < b:
                return b
            else:
                return a
        return None

    @staticmethod
    def compare_to(a: int, b: int):
        if a > b:
            return 1
        elif a < b:
            return -1
        else:
            return 0

    @staticmethod
    def bigint_comp(a: int, op: ScriptOp):
        if op == ScriptOp.NZ:
            return PushData.compare_to(a, 0) != 0
        return False

    @staticmethod
    def bigint_op(a: int, op: ScriptOp):
        if op == ScriptOp.INC:
            return a + 1
        elif op == ScriptOp.DEC:
            return a - 1
        elif op == ScriptOp.NEGATE:
            return -a
        elif op == ScriptOp.ABS:
            return a.__abs__()
        return a

    @staticmethod
    def hash(bs: bytearray, engine):
        if engine.op_code == ScriptOp.SHA1:
            return None
        elif engine.op_code == ScriptOp.SHA256:
            return Digest.sha256(bs)
        elif engine.op_code == ScriptOp.HASH160:
            return Digest.hash160(bs)
        elif engine.op_code == ScriptOp.HASH256:
            return Digest.hash256(bs)
        return None

    @staticmethod
    def pop_array(engine):
        return engine.evaluation_stack.pop().get_array()

    @staticmethod
    def pop_bytearray(engine):
        return engine.evaluation_stack.pop().get_bytearray()

    @staticmethod
    def pop_stack_item(engine):
        return engine.evaluation_stack.pop()

    @staticmethod
    def peek_stack_item(engine):
        return engine.evaluation_stack.peek(0)

    @staticmethod
    def pop_int(engine):
        item = engine.evaluation_stack.pop()
        return item.get_biginteger()

    @staticmethod
    def push(engine, ele: StackItems):
        engine.evaluation_stack.push(ele)

    @staticmethod
    def pop_bool(engine):
        return engine.evaluation_stack.pop().get_bool()

    @staticmethod
    def evaluation_stack_count(engine):
        return engine.evaluation_stack.count()

    @staticmethod
    def pop_interop_interface(engine):
        res = engine.evaluation_stack.pop()
        print(res)
        print(type(res))
        return res.get_interface()


    @staticmethod
    def peek_biginteger(engine):
        return PushData.peek_stack_item(engine).get_biginteger()

    @staticmethod
    def peek_n_stack_item(i: int, engine):
        return engine.evaluation_stack.peek(i)

    @staticmethod
    def count(engine):
        return engine.evaluation_stack.count()





