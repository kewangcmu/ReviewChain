# register a (owner, product) pair on supply chain system(simplified version)

# input: ownerkey_file, start from id

import json
import web3

from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys

# Load configurations in supplyChainContract.py
from supplyChainContract import supply_source_code, scontract_address
from supplyChainContract import sw3 as w3


if __name__ == '__main__':
    compiled_sol = compile_source(supply_source_code)
    contract_interface = compiled_sol['<stdin>:supplyChain']

    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    
    contract_instance = w3.eth.contract(
        scontract_address, abi=contract_interface['abi'], ContractFactoryClass=ConciseContract
    )

    ownerkey = open(sys.argv[1], "rb").read()
    startfrom = sys.argv[2]

    for i in range(startfrom,startfrom+1000):
        contract_instance.enrollProduct(i+274877906944, ownerkey, transact={'from': w3.eth.accounts[0], 'gas': 1000000})




