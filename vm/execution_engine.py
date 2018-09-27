from utils.push_data import PushData
from utils.script_op import ScriptOp
from vm.execution_context import ExecutionContext
from vm.op_exec_list import OpExecList
from vm.random_access_stack import RandomAccessStack
from vm.vm_state import VMState


class ExecutionEngine(object):
    def __init__(self):
        self.evaluation_stack = RandomAccessStack()
        self.alt_stack = RandomAccessStack()
        self.state = None
        self.contexts = list()
        self.context = None
        self.op_code = None
        self.op_code_value = None
        self.op_exec = None

    def current_context(self):
        if len(self.contexts) == 0:
            return None
        return self.contexts[len(self.contexts) - 1]

    def pop_context(self):
        if len(self.contexts) > 0:
            self.contexts.remove(self.contexts[len(self.contexts) - 1])
        self.context = self.current_context()

    def push_context(self, ctx: ExecutionContext):
        self.contexts.append(ctx)
        self.context = ctx

    def execute(self):
        self.state = VMState.value_of(self.state.value) & VMState.BREAK.value
        while True:
            if self.state == VMState.FAULT or self.state == VMState.HALT or self.state == VMState.BREAK:
                break
            if not self.step_info():
                return False

    def execute_code(self):
        code = self.context.op_reader.reader.read_byte()
        self.op_code = ScriptOp.value_of(code)
        self.op_code_value = code
        return True

    def validate_op(self):
        self.op_exec = OpExecList.get_op_exec(self.op_code)
        if self.op_exec is None:
            print(self.op_code, "does not support the operation code")
            return False
        return True

    def step_info(self):
        try:
            self.state = self.execute_op()
            return True
        except Exception as e:
            print(e)
            return False

    def execute_op(self):
        if ScriptOp.OP_PUSHBYTES1.value <= self.op_code_value <= ScriptOp.OP_PUSHBYTES75.value:
            PushData.push_data(self, self.context.op_reader.read_bytes(self.op_code_value))
            return VMState.NONE
        if not self.op_exec.validator(self):
            return VMState.FAULT
        return self.op_exec.exec(self)