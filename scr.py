import time
from web3 import Web3
from config import rpc, private_key


class SushiSwap():
    def __init__(self):
        self.rpc = rpc  # your node or use public rpc
        self.web3 = Web3(Web3.HTTPProvider(self.rpc))  # connect to web3
        # Setup Wallet Informations and RPC
        # Usually we place these info in separate .env or .py or .json file.
        self.pk = "d958dbe59f2c39b35487f581d0a5eca3c73dcc36022f35317437666a8193222b"  # your wallet private key
        # self.wallet = Web3.to_checksum_address(self.web3.eth.account.from_key(private_key=self.pk))  # your wallet address
        self.wallet = Web3.to_checksum_address("0xE2FFd8E80E3f4aaBeC6Ac4786e164C1a5efA17b4")  # your wallet address

        # Setup Swap Value / Gas limit / Gwei
        # Change these values if you want.
        self.buy_amount = 0  # Ether value to spend
        self.gas = 500000  # gas limit
        self.gwei = 5  # gwei

        # Setup WETH token address (to spend) and Token address (to buy)
        # In my case I'll use WBNB to buy Safemoon token (at BSC Testnet)
        self.token_to_swap = self.web3.to_checksum_address("0xdd69db25f6d620a7bad3023c5d32761d353d3de9")
        self.token_to_buy = self.web3.to_checksum_address("0x07865c6E87B9F70255377e024ace6630C1Eaa37F")

        # Setup router address (Sushiswap Router Address)
        # In my case I'll use Pancakeswap Router (at BSC Testnet)
        self.router = self.web3.to_checksum_address("0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506")

        self.abi = [{"inputs": [{"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                                 {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
                                 {"internalType": "address[]", "name": "path", "type": "address[]"},
                                 {"internalType": "address", "name": "to", "type": "address"},
                                 {"internalType": "uint256", "name": "deadline", "type": "uint256"}],
                      "name": "swapExactTokensForTokens",
                      "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
                      "stateMutability": "nonpayable", "type": "function"}]

        # Creating instance.
        # We can call contract functions with this.
        self.router_contract = self.web3.eth.contract(address=self.router, abi=self.abi)

        # Do swap.
        self.swap()

    # From here we are going to create Swap function.
    def swap(self, increase_gas=1.1):
        # building transaction with swap parameters
        # you can edit this if you want
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

        # Sign swap tx and send to blockchain
        sign_tx = self.web3.eth.account.sign_transaction(swap_txn, private_key=self.pk)
        buy_tx = self.web3.eth.send_raw_transaction(sign_tx.rawTransaction)
        print("Txn sent, awaiting for response.")

        # Await for result
        tx_result = self.web3.eth.wait_for_transaction_receipt(buy_tx)

        # Transaction status verification
        # If status == 1: Swap success.
        if tx_result['status'] == 1:
            print("Success! TX:", self.web3.to_hex(buy_tx))
            return True
        else:
            print("Error! TX:", self.web3.to_hex(buy_tx))
            return False


SushiSwap()