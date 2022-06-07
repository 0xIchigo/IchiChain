from p2pnetwork.node import Node
from blockchain_utils import BlockchainUtils
from peer_discovery_handler import PeerDiscoveryHandler
from socket_connector import SocketConnector
import json

# This class allows us to create peer-to-peer communication via socket communication - a subclass of Node


class SocketCommunication(Node):

    def __init__(self, ip, port):
        # Refers to the constructor of the Node class
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peer_discovery_handler = PeerDiscoveryHandler(self)
        self.socket_connector = SocketConnector(ip, port)

    # Connects the target node to the genesis node
    def connect_to_first_node(self):
        if self.socket_connector.port != 10001:
            self.connect_with_node("localhost", 10001)

    # Begins socket communication
    def start_socket_communication(self, node):
        self.node = node
        self.start()
        self.peer_discovery_handler.start()
        self.connect_to_first_node()

    # We get the inbound callback every time another node tries to connect to this specific instance of node
    def inbound_node_connected(self, connected_node):
        self.peer_discovery_handler.handshake(connected_node)

    # If you are the node that wants to connect to another node then you'll end up with the outbound callback
    def outbound_node_connected(self, connected_node):
        self.peer_discovery_handler.handshake(connected_node)

    # Regenerates the original message object via decoding
    def node_message(self, connected_node, message):
        message = BlockchainUtils.decode(json.dumps(message))
        if message.message_type == "DISCOVERY":
            self.peer_discovery_handler.handle_message(message)
        elif message.message_type == "TRANSACTION":
            transaction = message.data
            self.node.handle_transaction(transaction)
        elif message.message_type == "BLOCK":
            block = message.data
            self.node.handle_block(block)
        elif message.message_type == "BLOCKCHAINREQUEST":
            self.node.handle_blockchain_request(connected_node)
        elif message.message_type == "BLOCKCHAIN":
            blockchain = message.data
            self.node.handle_blockchain(blockchain)

    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)
