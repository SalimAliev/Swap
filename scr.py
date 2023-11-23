import time
from web3 import Web3
from config_local import rpc, private_key


class SushiSwap():
    def __init__(self):
        self.rpc = rpc
        self.web3 = Web3(Web3.HTTPProvider(self.rpc))

        self.pk = private_key
        self.wallet = Web3.to_checksum_address("0xE2FFd8E80E3f4aaBeC6Ac4786e164C1a5efA17b4")  # your wallet address

        self.buy_amount = 0  # Ether value to spend
        self.gas = 1000000  # gas limit
        self.gwei = self.web3.eth.gas_price  # gwei

        self.token_to_swap = self.web3.to_checksum_address("0x19E507da4DEF09910817c9Bd1026b17760f5196D")
        self.token_to_buy = self.web3.to_checksum_address("0x07865c6E87B9F70255377e024ace6630C1Eaa37F")

        self.router = self.web3.to_checksum_address("0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506")

        self.abi = [{"inputs": [{"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                                 {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
                                 {"internalType": "address[]", "name": "path", "type": "address[]"},
                                 {"internalType": "address", "name": "to", "type": "address"},
                                 {"internalType": "uint256", "name": "deadline", "type": "uint256"}],
                      "name": "swapExactTokensForTokens",
                      "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
                      "stateMutability": "nonpayable", "type": "function"}]

        self.router_contract = self.web3.eth.contract(address=self.router, abi=self.abi)

        self.swap()

    def swap(self):

        swap_txn = self.router_contract.functions.swapExactTokensForTokens(
            1,  # amountIn
            1,  # amountOutMin(slippage)
            [self.token_to_swap, self.token_to_buy],  # path (TOKEN,TOKEN)
            self.wallet,  # to (your wallet)
            (int(time.time()) + 10000)  # Deadline
        ).build_transaction({
            'from': self.wallet,
            'value': self.web3.to_wei(self.buy_amount, 'ether'),
            'gas': self.gas,
            'gasPrice': self.web3.to_wei(self.gwei,'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.wallet),
        })

        sign_tx = self.web3.eth.account.sign_transaction(swap_txn, private_key=self.pk)
        buy_tx = self.web3.eth.send_raw_transaction(sign_tx.rawTransaction)
        print("Txn sent, awaiting for response.")

        tx_result = self.web3.eth.wait_for_transaction_receipt(buy_tx)

        if tx_result['status'] == 1:
            print("Success! TX:", self.web3.to_hex(buy_tx))
            return True
        else:
            print("Error! TX:", self.web3.to_hex(buy_tx))
            return False


SushiSwap()