from ontology.common.address import Address


class Config(object):
    def __init__(self):
        self.contract_address = 'ContractAddress'
        self.storage_map = dict()
        self.tx = None

    def get_storage_map(self):
        return self.storage_map

    def get_signature_addresses(self):
        if self.tx.sigs is None:
            return None
        l = list()
        for i in range(len(self.tx.sigs)):
            for j in range(len(self.tx.sigs[i].public_keys)):
                if self.tx.sigs[i].M == 1:
                    address = Address.address_from_bytes_pubkey(self.tx.sigs[i].public_keys[0])
                    l.append(address.b58encode())
        return l

