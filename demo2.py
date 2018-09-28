from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.sig import Sig
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from src.types.bool_item import BoolItem
from src.types.bytearray_item import ByteArrayItem
from src.types.integer_item import IntegerItem
from src.utils.config import Config
from src.utils.script_op import ScriptOp
from src.utils.service_map import ServiceMap
from src.vm.execution_context import ExecutionContext
from src.vm.execution_engine import ExecutionEngine

privatekey1 = "1094e90dd7c4fdfd849c14798d725ac351ae0d924b29a279a9ffa77d5737bd96"
privatekey2 = "bc254cf8d3910bc615ba6bf09d4553846533ce4403bc24f58660ae150a6d64cf"
nep5abi = {"hash":"0x5bb169f915c916a5e30a3c13a5e0cd228ea26826","entrypoint":"Main","functions":
    [{"name":"Name","parameters":[],"returntype":"String"},{"name":"Symbol","parameters":[],"returntype":"String"},
     {"name":"Decimals","parameters":[],"returntype":"Integer"},{"name":"Main","parameters":
        [{"name":"operation","type":"String"},{"name":"args","type":"Array"}],"returntype":"Any"},
     {"name":"Init","parameters":[],"returntype":"Boolean"},{"name":"TotalSupply","parameters":[],"returntype":"Integer"},
     {"name":"Transfer","parameters":[{"name":"from","type":"ByteArray"},{"name":"to","type":"ByteArray"},
                                      {"name":"value","type":"Integer"}],"returntype":"Boolean"},
     {"name":"BalanceOf","parameters":[{"name":"address","type":"ByteArray"}],"returntype":"Integer"}],"events":[
    {"name":"transfer","parameters":[{"name":"arg1","type":"ByteArray"},{"name":"arg2","type":"ByteArray"},{"name":"arg3","type":"Integer"}],"returntype":"Void"}]}

codeStr = "57c56b6c766b00527ac46c766b51527ac4616c766b51c300c36c766b52527ac46c766b51c351c36c766b53527ac46c766b51c352c36c766b54527ac46c766b52c361681b53797374656d2e52756e74696d652e436865636b5769746e657373009c6c766b55527ac46c766b55c3643400610c3d3d3d6661696c3d3d3d3d3d61681253797374656d2e52756e74696d652e4c6f6761026e6f6c766b56527ac46222006c766b52c36c766b53c36c766b54c36152726516006c766b56527ac46203006c766b56c3616c756657c56b6c766b00527ac46c766b51527ac46c766b52527ac461536c766b53527ac461681953797374656d2e53746f726167652e476574436f6e746578746c766b54527ac46c766b54c306726573756c74062d7474657374615272681253797374656d2e53746f726167652e507574616c766b54c306726573756c74617c681253797374656d2e53746f726167652e4765746c766b55527ac40e3d3d737563636573733d3d3d3d3d61681253797374656d2e52756e74696d652e4c6f6761616c766b00c36c766b51c36c766b52c3615272087472616e7366657254c1681553797374656d2e52756e74696d652e4e6f74696679616c766b55c36c766b56527ac46203006c766b56c3616c7566";

sdk = OntologySdk()


def execute_test():
    acct1 = Account(privatekey1)
    acct2 = Account(privatekey2)
    abi = AbiInfo(nep5abi['hash'], nep5abi['entrypoint'], nep5abi["functions"])
    func = abi.get_function("Transfer")
    func.set_params_value((acct1.get_address().to_array(), acct2.get_address().to_array(),19*10000000))
    func.name = func.name.lower()
    params = BuildParams.serialize_abi_function(func)
    params += bytearray([0x67])
    print("params: ", params.hex())
    code_bytes = bytearray.fromhex(codeStr)
    engine = ExecutionEngine()
    engine.push_context(ExecutionContext(engine, params))
    config = Config()
    contractAddress = Address.address_from_vm_code(codeStr)
    config.tx = sdk.neo_vm().make_invoke_transaction(contractAddress.to_array(), params, None, 0, 0)
    tx_hash = config.tx.hash256_bytes()
    sig_data = acct1.generate_signature(tx_hash, acct1.get_signature_scheme())
    sig = Sig([acct1.serialize_public_key()], 1, [sig_data])
    config.tx.sigs = list()
    config.tx.sigs.append(sig)
    num = 0
    while(True):
        if len(engine.contexts) == 0:
            break
        engine.execute_code()
        if engine.op_code == ScriptOp.OP_RET:
            break
        if engine.op_code is None:
            pass
        elif ScriptOp.OP_PUSHBYTES1.value <= engine.op_code.value <= ScriptOp.OP_PUSHBYTES75.value:
            pass
        elif not engine.validate_op():
            break
        num += 1
        if engine.op_code is not None:
            print(num, "> " + str(engine.evaluation_stack.count()) + " " + hex(engine.op_code.value) + " " +  engine.op_exec.name + " " + engine.evaluation_stack.info())
        if ScriptOp.OP_APPCALL == engine.op_code:
            engine2 = ExecutionEngine()
            engine2.push_context(ExecutionContext(engine2, code_bytes))
            engine.evaluation_stack.copy_to(engine2.evaluation_stack)
            engine = engine2
        elif ScriptOp.OP_SYSCALL == engine.op_code:
            bys = engine.context.op_reader.read_var_bytes()
            print("####SYSCALL####", bys.decode())
            service = ServiceMap.get_service(bys.decode())
            if service is None:
                print(bys.decode())
                return
            service.exec(config, engine)
        else:
            engine.step_info()
    print("##########end############")
    print("Stack Count:", engine.evaluation_stack.count())
    items = engine.evaluation_stack.peek(0)
    if type(items) is ByteArrayItem:
        print("Result ByteArrayItem:", engine.evaluation_stack.peek(0).get_bytearray().hex() + engine.evaluation_stack.peek(0).get_bytearray().decode())
    elif type(items) is IntegerItem:
        print("Result GetBigInteger:", engine.evaluation_stack.peek(0).get_biginteger())
    elif type(items) is BoolItem:
        print("Result BoolItem:", engine.evaluation_stack.peek(0).get_bool())
    return


if __name__ == "__main__":
    execute_test()
