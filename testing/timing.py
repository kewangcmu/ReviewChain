import json
import web3

from web3 import Web3, HTTPProvider, IPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import time
import sys

from ecdsa import SigningKey, VerifyingKey, BadSignatureError
from reviewContractN import contract_source_code, contract_address, w3

# input: previous, save file name

PREVIOUS = int(sys.argv[1])

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

    submitted_l = contract_instance.eventFilter('NewReviewSubmitted', {'fromBlock':PREVIOUS,'toBlock':'latest'})
    voted_l = contract_instance.eventFilter('NotaryVoted', {'fromBlock':PREVIOUS,'toBlock':'latest'})
    confirmed_l = contract_instance.eventFilter('ReviewConfirmed', {'fromBlock':PREVIOUS,'toBlock':'latest'})

    s_l = submitted_l.get_all_entries()
    v_l = voted_l.get_all_entries()
    c_l = confirmed_l.get_all_entries()

    sv_total = 0
    vc_total = 0
    throughput_dic = {}

    avg_s = 0
    avg_v = 0
    avg_c = 0

    dic = {}
    startb_s = s_l[0].blockNumber
    for s in s_l:
        dic[s.args.epc] = [s.args.time]
        stopb_s = s.blockNumber
        avg_s = avg_s + s.args.time/2000

    startb_v = v_l[0].blockNumber
    for v in v_l:
        dic[v.args.epc].append(v.args.time)
        stopb_v = v.blockNumber
        avg_v = avg_v + v.args.time/6000

    startb_c = c_l[0].blockNumber
    for c in c_l:
        dic[c.args.epc].append(c.args.time)
        if c.args.time-s_l[0].args.time in throughput_dic:
            throughput_dic[c.args.time-s_l[0].args.time] = throughput_dic[c.args.time-s_l[0].args.time] + 1
        else:
            throughput_dic[c.args.time-s_l[0].args.time] = 1

        stopb_c = c.blockNumber
        stopt_c = c.args.time
        avg_c = avg_c + c.args.time/2000

    with open(sys.argv[2], 'a') as the_file:
        for key, value in dic.items():
            #sv_total += (value[1] - value[0])
            #vc_total += (value[-1] - value[1])
            vc_total += value[-1]

            the_file.write(str(key) + ", " + str(value) + "\n")

        the_file.write("endblock\n")
        the_file.write("submission block frame\n")
        the_file.write(str(startb_s) + " - " + str(stopb_s) + "\n")
        the_file.write("notary block frame\n")
        the_file.write(str(startb_v) + " - " + str(stopb_v) + "\n")
        the_file.write("confirm block frame\n")
        the_file.write(str(startb_c) + " - " + str(stopb_c) + "\n")
        the_file.write("block interval\n")
        the_file.write(str((stopt_c - s_l[0].args.time)/(stopb_c - startb_s)) + "\n")
        the_file.write("average sv, vc\n")
        the_file.write(str(sv_total/2000) + ", " + str(vc_total/2000) + "\n")
        the_file.write("latency, throughput\n")
        the_file.write(str((sv_total+vc_total)/2000) + ", " + str(2000/(stopt_c - c_l[0].args.time)) + "\n")
        the_file.write("avg_s,v,c\n")
        the_file.write(str(avg_s) + ", " + str(avg_v) + ", " + str(avg_c))

    with open(sys.argv[2]+".throuput", 'a') as the_file:
        for i in range(0,stopt_c-s_l[0].args.time+1):
            if i in throughput_dic:
                the_file.write(str(i) + "," + str(throughput_dic[i]) + "\n")
            else:
                the_file.write(str(i) + ",0" + "\n")




