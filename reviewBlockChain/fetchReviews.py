# fetch all reviews associated with a specific product type (epc>>38)

# input: product type (int)

import json
import web3
import sys

from web3 import Web3, HTTPProvider, IPCProvider
from solc import compile_source
from web3.contract import ConciseContract
from reviewContractN import contract_source_code, contract_address, w3


if __name__ == '__main__':

    input = sys.argv[1]

    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:reviewSystem']

    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    contract_instance = w3.eth.contract(
        contract_address, abi=contract_interface['abi'], ContractFactoryClass=ConciseContract
    )

    # contract_instance.registerProduct('abcdef', 2, transact={'from': w3.eth.accounts[0]})

    id = int(input)
    print("id = " + str(id))
    # try:
    # print("if exist: " + str(contract_instance.ifHasProduct(id)))
    print("review count: " + str(contract_instance.getReviewCount(id)))
    print("")

    # id, epc, rating, content
    # with open("reviews.txt", 'a') as f:
    #     for i in range(0, contract_instance.getReviewCount(id)):
    #         rating, content, epc = contract_instance.getReview(id, i)
    #         f.write(str(id) + ", " + str(epc) + ", " + str(rating) + ", " + content + "\n")

    for i in range(0, contract_instance.getReviewCount(id)):
        rating, content, EPC = contract_instance.getReview(id, i)
        print("Review #: " + str(i) + "\nRating: " + str(rating) + "\nContent: " + content + "\nEPC: " + str(EPC))
        print("===============")
    


# if contract_instance.ifHasProduct(id):
#     contract_instance.addReview(id, 1, "so bad!", transact={'from': w3.eth.accounts[0]})
