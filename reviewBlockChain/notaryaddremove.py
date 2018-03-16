# delete a notary from the review Sytem by admin

#input: notary account index


import json
import web3

from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract

from reviewContractN import contract_source_code, contract_address, w3
import sys

NOTARY = int(sys.argv[1])

if __name__ == '__main__':
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:reviewSystem']

    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    contract_instance = w3.eth.contract(
        contract_address, abi=contract_interface['abi']
    )

    conciseC_instance = w3.eth.contract(
        contract_address, abi=contract_interface['abi'], ContractFactoryClass=ConciseContract
    )

    conciseC_instance.notaryRemove(w3.eth.accounts[NOTARY], transact={'from': w3.eth.accounts[0], 'gas': 1000000})

    stop = input("wait for miner to mine:")

    print(conciseC_instance.notaryCount())