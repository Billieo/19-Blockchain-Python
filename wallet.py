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
print(BTC)

from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3 import Web3, middleware, Account
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware
# connect Web3
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
# enable PoA middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# set gas price strategy to built-in "medium" algorithm (est ~5min per tx)
# see https://web3py.readthedocs.io/en/stable/gas_price.html?highlight=gas
# see https://ethgasstation.info/ API for a more accurate strategy
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
 
 
# Create a function called `derive_wallets`
myMnemonic = "milk dress vote orange diesel cigar reject start fury genius remind dose"


def derive_wallets(mnemonic=myMnemonic, coin=BTC, numderive=3,):
    command = f"php ./hd-wallet-derive/hd-wallet-derive.php -g --mnemonic=\"{mnemonic}\" --coin={coin} --numderive={numderive} --cols=path,address,privkey --format=json"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    print(command)
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    ETH:derive_wallets(myMnemonic,ETH,3),
    BTCTEST:derive_wallets(myMnemonic,BTCTEST,3)
}
print(coins)


# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    # YOUR CODE HERE
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        print(priv_key)
        return PrivateKeyTestnet(priv_key)


# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.

def create_tx(coin, account, to, amount):
    if coin == ETH:
        value = w3.toWei(amount, "ether") 
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": value}
        )
        return {
            "from": account.address,
            "to": to,
            "value": value,
            "gasPrice": w3.eth.generateGasPrice(),
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account),
            "chainId": w3.eth.chain_id
        }
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    if coin == ETH:
        tx = create_tx(coin, account, to, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result)
        return result
    if coin == BTCTEST:
        tx = create_tx(coin, account, to, amount)
        signed_tx = account.sign_transaction(tx)
        result = NetworkAPI.broadcast_tx_testnet(signed_tx)
        print(result)
        return result

    