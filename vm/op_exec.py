import os

from utils.script_op import ScriptOp
from vm.vm_state import VMState


class OpExec(object):

    def __init__(self, op_code: ScriptOp, name: str, exec_func, validator_func):
        self.op_code = op_code
        self.name = name
        self.exec_func = exec_func
        self.validator_func = validator_func

    def exec(self, engine):
        try:
            if self.exec_func is None:
                return VMState.NONE
            self.exec_func(engine)
        except Exception as e:
            print(e)
            os._exit(0)
        return VMState.NONE

    def validator(self, engine):
        if self.validator_func is None:
            return True
        try:
            self.validator_func(engine)
        except Exception as e:
            print(e)
            os._exit()
        return False