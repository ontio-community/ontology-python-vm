from src.utils.vm_reader import VmReader


class ExecutionContext(object):
    def __init__(self, engine, code: bytearray):
        self.code = code
        self.engine = engine
        self.op_reader = VmReader(code)
        self.instruction_pointer = 0

    def get_instruction_pointer(self):
        return self.op_reader.position()

    def set_instruction_pointer(self, offset: int):
        self.op_reader.seek(offset)

    def clone(self):
        execution_context = ExecutionContext(self.engine, self.code)
        execution_context.instruction_pointer = self.instruction_pointer
        execution_context.set_instruction_pointer(self.get_instruction_pointer())
        return execution_context

