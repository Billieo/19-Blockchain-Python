# 19-Blockchain-Python

- The neccessary library was imported

- Hd wallet was clone from 
    [github](https://github.com/dan-da/hd-wallet-derive/)

- A constant.py file was also created which consist of my varable(BTC = 'btc', ETH = 'eth',BTCTEST = 'btc-test') that will be called in the wallet.py

- A derive wallet function was created that use the mnemonic pharse.

- A a dictionary object was also created to store the out put from the derive wallet for is btc and eth.

- Bit and web3.py were used to leverage the keys stored in the coins along with the below functions

- A priv_key_to_account funtion in which we parse coin and priv_key was created using an if statment to convert the privkey to a string.

- creat_tx function was created using the following code
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
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)]).

- send_tx function was created using the following code        
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


- To send the btc transaction the following code was executed
send_tx(BTCTEST, account, 'n1kUxYxiTfsTizXZBHPCkH2qd4XiACrWUf', '0.0001')

BTC transaction
![alttext](image/Bitcoin1.png)


![alttext](image/Bitcoin2.png)


![alttext](image/Btctranscode.png)
