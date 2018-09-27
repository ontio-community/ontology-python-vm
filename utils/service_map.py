
from utils.service import Service


class ServiceMap(object):
    ATTRIBUTE_GETUSAGE_NAME = "Ontology.Attribute.GetUsage"
    ATTRIBUTE_GETDATA_NAME = "Ontology.Attribute.GetData"
    BLOCK_GETTRANSACTIONCOUNT_NAME = "System.Block.GetTransactionCount"
    BLOCK_GETTRANSACTIONS_NAME = "System.Block.GetTransactions"
    BLOCK_GETTRANSACTION_NAME = "System.Block.GetTransaction"
    BLOCKCHAIN_GETHEIGHT_NAME = "System.Blockchain.GetHeight"
    BLOCKCHAIN_GETHEADER_NAME = "System.Blockchain.GetHeader"
    BLOCKCHAIN_GETBLOCK_NAME = "System.Blockchain.GetBlock"
    BLOCKCHAIN_GETTRANSACTION_NAME = "System.Blockchain.GetTransaction"
    BLOCKCHAIN_GETCONTRACT_NAME = "System.Blockchain.GetContract"
    BLOCKCHAIN_GETTRANSACTIONHEIGHT_NAME = "System.Blockchain.GetTransactionHeight"
    HEADER_GETINDEX_NAME = "System.Header.GetIndex"
    HEADER_GETHASH_NAME = "System.Header.GetHash"
    HEADER_GETVERSION_NAME = "Ontology.Header.GetVersion"
    HEADER_GETPREVHASH_NAME = "System.Header.GetPrevHash"
    HEADER_GETTIMESTAMP_NAME = "System.Header.GetTimestamp"
    HEADER_GETCONSENSUSDATA_NAME = "Ontology.Header.GetConsensusData"
    HEADER_GETNEXTCONSENSUS_NAME = "Ontology.Header.GetNextConsensus"
    HEADER_GETMERKLEROOT_NAME = "Ontology.Header.GetMerkleRoot"
    TRANSACTION_GETHASH_NAME = "System.Transaction.GetHash"
    TRANSACTION_GETTYPE_NAME = "Ontology.Transaction.GetType"
    TRANSACTION_GETATTRIBUTES_NAME = "Ontology.Transaction.GetAttributes"
    CONTRACT_CREATE_NAME = "Ontology.Contract.Create"
    CONTRACT_MIGRATE_NAME = "Ontology.Contract.Migrate"
    CONTRACT_GETSTORAGECONTEXT_NAME = "System.Contract.GetStorageContext"
    CONTRACT_DESTROY_NAME = "System.Contract.Destroy"
    CONTRACT_GETSCRIPT_NAME = "Ontology.Contract.GetScript"
    STORAGE_GET_NAME = "System.Storage.Get"
    STORAGE_PUT_NAME = "System.Storage.Put"
    STORAGE_DELETE_NAME = "System.Storage.Delete"
    STORAGE_GETCONTEXT_NAME = "System.Storage.GetContext"
    STORAGE_GETREADONLYCONTEXT_NAME = "System.Storage.GetReadOnlyContext"
    STORAGECONTEXT_ASREADONLY_NAME = "System.StorageContext.AsReadOnly"
    RUNTIME_GETTIME_NAME = "System.Runtime.GetTime"
    RUNTIME_CHECKWITNESS_NAME = "System.Runtime.CheckWitness"
    RUNTIME_NOTIFY_NAME = "System.Runtime.Notify"
    RUNTIME_LOG_NAME = "System.Runtime.Log"
    RUNTIME_GETTRIGGER_NAME = "System.Runtime.GetTrigger"
    RUNTIME_SERIALIZE_NAME = "System.Runtime.Serialize"
    RUNTIME_DESERIALIZE_NAME = "System.Runtime.Deserialize"
    NATIVE_INVOKE_NAME = "Ontology.Native.Invoke"
    GETSCRIPTCONTAINER_NAME = "System.ExecutionEngine.GetScriptContainer"
    GETEXECUTINGSCRIPTHASH_NAME = "System.ExecutionEngine.GetExecutingScriptHash"
    GETCALLINGSCRIPTHASH_NAME = "System.ExecutionEngine.GetCallingScriptHash"
    GETENTRYSCRIPTHASH_NAME = "System.ExecutionEngine.GetEntryScriptHash"
    APPCALL_NAME = "APPCALL"
    TAILCALL_NAME = "TAILCALL"
    SHA1_NAME = "SHA1"
    SHA256_NAME = "SHA256"
    HASH160_NAME = "HASH160"
    HASH256_NAME = "HASH256"
    UINT_DEPLOY_CODE_LEN_NAME = "Deploy.Code.Gas"
    UINT_INVOKE_CODE_LEN_NAME = "Invoke.Code.Gas"

    map = dict()

    @staticmethod
    def init():
        ServiceMap.map[ServiceMap.STORAGE_PUT_NAME] = Service(getattr(Service(),"storage_put"),None)
        ServiceMap.map[ServiceMap.STORAGE_GETCONTEXT_NAME] = Service(getattr(Service(), "storage_get_context"), None)
        ServiceMap.map[ServiceMap.STORAGE_GET_NAME] = Service(getattr(Service(), "storage_get"), None)
        ServiceMap.map[ServiceMap.RUNTIME_LOG_NAME] = Service(getattr(Service(), "runtime_log"), None)
        ServiceMap.map[ServiceMap.RUNTIME_NOTIFY_NAME] = Service(getattr(Service(), "runtime_notify"), None)
        ServiceMap.map[ServiceMap.RUNTIME_CHECKWITNESS_NAME] = Service(getattr(Service(), "runtime_check_witness"), None)
        ServiceMap.map[ServiceMap.RUNTIME_DESERIALIZE_NAME] = Service(getattr(Service(), "runtime_deserialize"), None)
        ServiceMap.map[ServiceMap.RUNTIME_SERIALIZE_NAME] = Service(getattr(Service(), "runtime_serialize"),None)

    @staticmethod
    def get_service(key: str):
        if len(ServiceMap.map) == 0:
            ServiceMap.init()
        return ServiceMap.map[key]



