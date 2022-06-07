from transaction_pool import TransactionPool
from wallet import Wallet
from blockchain import Blockchain
from socket_communication import SocketCommunication
from node_api import NodeAPI
from message import Message
from blockchain_utils import BlockchainUtils
import copy

# Blockchain nodes refer to a network's stakeholders and/or their devices (often a computer),
# which keep a copy of the distributed ledger and serve as a communication point that executes various network functions
# A node's main purpose is to verify the validity of each succeeding block
# Nodes form the very infrastructure of the blockchain as both participants and managing entities


class Node():

    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transaction_pool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()

        # Creates nodes based on serialized key files
        if key is not None:
            self.wallet.from_key(key)

    def start_p2p(self):
        # Defined here so we have more flexibility and nodes do not have to start immediately
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self)

    def start_api(self, api_port):
        self.api = NodeAPI()
        # Providing the initialized node found above to our API
        self.api.inject_node(self)
        self.api.start(api_port)

    # Returns whether the transaction is valid and if the transaction is not already in the transaction pool
    def handle_transaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key
        signature_valid = Wallet.signature_valid(
            data, signature, signer_public_key)
        transaction_exists = self.transaction_pool.transaction_exists(
            transaction)
        transaction_in_block = self.blockchain.transaction_exists(transaction)
        if not transaction_exists and not transaction_in_block and signature_valid:
            self.transaction_pool.add_transaction(transaction)
            # Propagating the transaction to the network
            message = Message(self.p2p.socket_connector,
                              "TRANSACTION", transaction)
            encoded_message = BlockchainUtils.encode(message)
            self.p2p.broadcast(encoded_message)
            # Checking if it is time to generate a new block
            forging_required = self.transaction_pool.forger_required()
            if forging_required:
                self.forge()

    def handle_block(self, block):
        forger = block.forger
        block_hash = block.payload()
        signature = block.signature

        # Checking the block count, hash, forger, signature, timestamp, and transactions are all valid
        block_count_valid = self.blockchain.block_count_valid(block)
        prev_block_hash = self.blockchain.prev_block_hash_valid(block)
        forger_valid = self.blockchain.forger_valid(block)
        signature_valid = Wallet.signature_valid(block_hash, signature, forger)
        timestamp_valid = self.blockchain.timestamp_valid(block.timestamp)
        transaction_valid = self.blockchain.transaction_valid(
            block.transactions)

        # If a node joins later it'll request the existing blocks to maintain one valid blockchain state
        if not block_count_valid:
            self.request_chain()

        # If the block is valid, we push it to the chain and propagate it to the network
        if block_count_valid and prev_block_hash and forger_valid and signature_valid and transaction_valid and timestamp_valid:
            self.blockchain.add_block(block)
            self.transaction_pool.remove_from_pool(block.transactions)
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            encoded_message = BlockchainUtils.encode(message)
            self.p2p.broadcast(encoded_message)

    # Requests the current blockchain state from other nodes
    def request_chain(self):
        message = Message(self.p2p.socket_connector, "BLOCKCHAINREQUEST", None)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.broadcast(encoded_message)

    # Handles a node's request for the current blockchain state
    def handle_blockchain_request(self, requesting_node):
        message = Message(self.p2p.socket_connector,
                          "BLOCKCHAIN", self.blockchain)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.send(requesting_node, encoded_message)

    # Handles if a node disconnects from, or connects for the first time to, the blockchain
    def handle_blockchain(self, blockchain):
        local_blockchain_copy = copy.deepcopy(self.blockchain)
        local_block_count = len(local_blockchain_copy.blocks)
        received_chain_block_count = len(blockchain.blocks)
        # Looping over new blocks, and not blocks the node already has
        if local_block_count < received_chain_block_count:
            for block_number, block in enumerate(blockchain.blocks):
                if block_number >= local_block_count:
                    # Building the blockchain up on this copy
                    local_blockchain_copy.add_block(block)
                    self.transaction_pool.remove_from_pool(block.transactions)
            self.blockchain = local_blockchain_copy

    def forge(self):
        forger = self.blockchain.next_forger()
        # If this specific node is chosen as the forger
        if forger == self.wallet.public_key_string():
            print("I am the next forger")
            # Creating the new block
            block = self.blockchain.create_block(
                self.transaction_pool.transactions, self.wallet)
            # Updating the transaction pool
            self.transaction_pool.remove_from_pool(block.transactions)
            # Encoding and broadcasting the new block to the network
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            encoded_message = BlockchainUtils.encode(message)
            self.p2p.broadcast(encoded_message)
        else:
            print("I am not the next forger")
