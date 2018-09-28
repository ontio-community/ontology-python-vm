from src.vm.execution_context import ExecutionContext
from src.vm.execution_engine import ExecutionEngine


def execute():
    code_str = "52c56b61536c766b00527ac46c766b00c36c766b51527ac46203006c766b51c3616c7566"
    code = bytearray.fromhex(code_str)
    engine = ExecutionEngine()
    ctx = ExecutionContext(engine, code)
    engine.push_context(ctx)
    while True:
        if len(engine.contexts) == 0 or engine.context is None:
            break
        engine.execute_code()
        if not engine.validate_op():
            break
        print(engine.evaluation_stack.count(), hex(engine.op_code.value) + "  " + engine.op_exec.name + "  " + engine.evaluation_stack.info())
        engine.step_info()
    print("Stack Count:", engine.evaluation_stack.count())
    print("Result:", engine.evaluation_stack.peek(0).get_biginteger())
    return


if __name__ == "__main__":
    execute()