# notary watcher
# notary start this program to process unconfirmed reviews in unconfirmed section.
# 1) listen for new events(new unconfirmed review enter unconfirmed section) created by review system
# 2) process the events in a set INTERVAL

# input: eth_account_index (notary account)

import json
import web3

from web3 import Web3, HTTPProvider, IPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import time
import sys

from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from reviewContractN import contract_source_code, contract_address, w3
from supplyChainContract import supply_source_code, scontract_address, sw3
import threading
# input: previous

# CONSTANT
NOTARY=int(sys.argv[3])
INTERVAL = float(sys.argv[2])
REFUNDABLE_TIME = 0

PREVIOUS = int(sys.argv[1])


timetostart = time.time() + 5

# query the supplychain block chain for owner id and sold time
def supplyBlockChainQuery(scontract_instance, epc):

    ownerid = scontract_instance.getCurrentOwner(epc)
    soldTime = scontract_instance.getcreationTime(epc)
    # print(contract_instance.getCurrentOwner(epc))
    # print(soldTime)

    return ownerid, soldTime

# verify signature: using ECDSA NIST192p 
def sigVerify(ownerid, epc, ownersig):
    vk = VerifyingKey.from_string(ownerid)

    try:
        vk.verify(ownersig, str(epc).encode())
        return True
    except BadSignatureError: 
        return False

# validation procedure
# 1) the epc exists in supply chain block chain
# 2) signature correct
# 3) time exceeds refundable time constraint
def checkValidity(scontract_instance, epc, ownersig):
    ownerid, soldTime = supplyBlockChainQuery(scontract_instance, epc)

    if ownerid:
        if sigVerify(ownerid, epc, ownersig) == False:
            return False
        elif time.time() - soldTime < REFUNDABLE_TIME:
            return False
        else:
            return True
    else:
        return False

def rt(contract_instance):
    # start watching for new events
    avg_s = 0
    previous = PREVIOUS

    time.sleep(timetostart-time.time())
    print("Start RT")
    while True:
        time.sleep(INTERVAL)

        listener = contract_instance.eventFilter('NewReviewSubmitted', {'fromBlock':previous,'toBlock':'latest'})

        newEvents = listener.get_all_entries()

        if newEvents:
            avg_s = avg_s + time.time()/2000*len(newEvents)
       
        for event in newEvents:
            previous = event.blockNumber + 1          
 
        if newEvents:
            print("rt::::::::avg_s:" + str(avg_s))


if __name__ == '__main__':

    # 1. construct review contract interface
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:reviewSystem']

    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    contract_instance = w3.eth.contract(
        contract_address, abi=contract_interface['abi']
    )

    conciseC_instance = w3.eth.contract(
        contract_address, abi=contract_interface['abi'], ContractFactoryClass=ConciseContract
    )

    # 2. construct supply chain contract interface
    scompiled_sol = compile_source(supply_source_code)
    scontract_interface = scompiled_sol['<stdin>:supplyChain']

    scontract = sw3.eth.contract(abi=scontract_interface['abi'], bytecode=scontract_interface['bin'])

    scontract_instance = sw3.eth.contract(
        scontract_address, abi=scontract_interface['abi'], ContractFactoryClass=ConciseContract
    )

    # timer test
    # a = time.time()
    # print(checkValidity(scontract_instance, 123456, open("sig.txt","rb").read()))
    # b = time.time()
    # print(b-a)
    

    threads = []
    for i in range(1):
        t = threading.Thread(target=rt, args=(contract_instance,))
        threads.append(t)
        t.start()

    # start watching for new events
    total = 0
    avg_s = 0
    avg_e = 0
    
    # same phase to experiment
    time.sleep(timetostart-time.time())
    print("Start Listening new review submission...")
    while True:
        time.sleep(INTERVAL)

        listener = contract_instance.eventFilter('NewReviewSubmitted', {'fromBlock':PREVIOUS,'toBlock':'latest'})
        
        newEvents = listener.get_all_entries()
        
        if newEvents:
            avg_s = avg_s + time.time()/2000*len(newEvents)
            start_t = time.time()

        for event in newEvents:
            epc = event.args.epc
            ownersig = event.args.ownersig[:48] # extract 48 bytes in 64 bytes to prevent extraction error
            result = checkValidity(scontract_instance, epc, ownersig)
            conciseC_instance.notarySendResult(epc, result, transact={'from': w3.eth.accounts[NOTARY], 'gas': 1000000})
            # ========= end processing a unconfirmed review ==========(timer: notary finish processing)
            avg_e = avg_e + time.time()/2000
            # print(w3.eth.accounts[int(sys.argv[1])] + ": " + str(epc) + ", " + str(ownersig) + ", " + str(result))
            PREVIOUS = event.blockNumber + 1
            # print("================" + str(previous))

        if newEvents:
            end_t = time.time()
            total = total + (end_t-start_t)
            print("timeUsed: " + str(end_t-start_t))
            print("start - end: " + str(start_t) + " - " + str(end_t))
            print("#: " + str(len(newEvents)))
            print("total time now: " + str(total))
            
            print("current avg_s, avg_e: " + str(avg_s) + " - " + str(avg_e))
            print("===============")
            




