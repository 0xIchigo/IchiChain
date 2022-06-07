from transactions import Transaction
from wallet import Wallet
from transaction_pool import TransactionPool
from block import Block
from blockchain import Blockchain
from blockchain_utils import BlockchainUtils
from account_model import AccountModel
from node import Node
import pprint
import sys

if __name__ == '__main__':

    # We use sys so we can provide arguments on the command line, such as the ip and port we want to run on
    # Argv[0] would be main.py, so we make the ip an index of 1, the port an index of 2, the API port an index of 3, and, the key file is an index of 4 if specified
    ip = sys.argv[1]
    port = int(sys.argv[2])
    api_port = int(sys.argv[3])
    key_file = None
    if len(sys.argv) > 4:
        key_file = sys.argv[4]

    node = Node(ip, port, key_file)
    node.start_p2p()
    node.start_api(api_port)
