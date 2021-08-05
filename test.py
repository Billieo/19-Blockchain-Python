# Import dependencies
import os
import subprocess
import json
from dotenv import load_dotenv


# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import *

from web3 import Web3
from web3.middleware import geth_poa_middleware
 

command = './derive -g --mnemonic="milk dress vote orange diesel cigar reject start fury genius remind dose" --cols=path,address,privkey,pubkey --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

