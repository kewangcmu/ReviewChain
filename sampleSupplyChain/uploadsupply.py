# Upload the supply chain contract to its networks

import json
import web3

from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract

# Load configurations in supplyChainContract.py
from supplyChainContract import supply_source_code, scontract_address
from supplyChainContract import sw3 as w3

 

if __name__ == '__main__':

    compiled_sol = compile_source(supply_source_code)
    contract_interface = compiled_sol['<stdin>:supplyChain']

    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 100000000})

    stop = input("wait for miner to mine:")

    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    contract_instance = w3.eth.contract(
        contract_address, abi=contract_interface['abi'], ContractFactoryClass=ConciseContract
    )
    print(tx_receipt)

