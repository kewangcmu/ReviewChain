# add one review through a python program

# input: privateKey_file (in bytes format), epc, rating, content

import json
import web3
import sys, csv
import time

from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract
from reviewContractN import contract_source_code, contract_address, w3

from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import threading

# input: start id of a product 

def submit(contract_instance, start_id, end_id):
    
    avg_e = 0
    start_t = time.time()
    for i in range(start_id,end_id):
        # use bytes encoded epc as signature message.
        # sign the epc use a private key
        sk = SigningKey.from_string(open(privateKey_file, 'rb').read())
        # sign and padding 48 bytes to 64 bytes to prevent extraction error
        sig = sk.sign(str(i+274877906944).encode()).ljust(64, b"\x0f") 
        time.sleep(0.01)
        # send transaction for adding a new review
        contract_instance.adduReview(int(i+274877906944), sig, rating, content, transact={'from': w3.eth.accounts[0], 'gas': 1000000})
        # (timer: review submitted)
        avg_e = avg_e + time.time()/2000
	
    end_t = time.time()
    print(str(start_id) + " - " + str(end_id) + ": " + str(start_t) + " - " + str(end_t))

    print("avg_endtime: " + str(avg_e))
    print("submission rate: " + str(2000/(end_t - start_t)))

if __name__ == '__main__':

    privateKey_file = 'sk.txt'
    startfrom = int(sys.argv[1])
    
    rating = 5
    content = "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee" + \
              "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee" + \
              "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee" + \
              "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee" + \
              "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee" + \
              "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee" + \
              "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee" + \
              "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee" + \
              "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee" + \
              "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee"
               

    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:reviewSystem']

    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    contract_instance = w3.eth.contract(
        contract_address, abi=contract_interface['abi'], ContractFactoryClass=ConciseContract
    )
    
    # multithread 
    #threads = []
    #for i in range(2):
     #   print("a")
      #  t = threading.Thread(target=submit, args=(contract_instance, startfrom, startfrom+500,))
       # threads.append(t)
#        t.start()
 #       startfrom = startfrom+500
    submit(contract_instance, startfrom, startfrom+1000)
