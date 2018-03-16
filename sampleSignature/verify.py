import sys
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import time

# ownerkey_f, epc_f, sig_f
if __name__ == "__main__":

    ownerkey = open(sys.argv[1], "rb").read()
    epc = sys.argv[2].encode()
    sig = open(sys.argv[3], "rb").read()


    for 
        vk = VerifyingKey.from_string(ownerkey)

    