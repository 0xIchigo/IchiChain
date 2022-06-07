from wallet import Wallet
from blockchain_utils import BlockchainUtils
import requests


def post_transaction(sender, receiver, amount, type):
    transaction = sender.create_transaction(
        receiver.public_key_string(), amount, type)

    url = "http://localhost:5000/transaction"
    package = {"transaction": BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.text)


# Test script
if __name__ == '__main__':
    bob = Wallet()
    alice = Wallet()
    alice.from_key("keys/stakerPrivateKey.pem")
    exchange = Wallet()

    # Forger: Genesis
    post_transaction(exchange, alice, 100, "EXCHANGE")
    post_transaction(exchange, bob, 100, "EXCHANGE")
    post_transaction(exchange, bob, 10, "EXCHANGE")

    # Forger: Probably Alice
    # Alice sends to herself as she is staking
    post_transaction(alice, alice, 25, "STAKE")
    post_transaction(alice, bob, 1, "TRANSFER")
    post_transaction(alice, bob, 1, "TRANSFER")

    # For testing purposes, run these commands in separate instances of command prompt
    # python main.py localhost 10001 5000 keys/genesisPrivateKey.pem
    # python main.py localhost 10002 5001
    # python main.py localhost 10003 5003 keys/stakerPrivateKey.pem - simulating Alice's computer
    # python interaction.py
