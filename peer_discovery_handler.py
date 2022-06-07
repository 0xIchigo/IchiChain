from message import Message
from blockchain_utils import BlockchainUtils
import threading
import time


# This class communicates with the network to see if new nodes are available or not
# This could've been put in socket_communication.py but it's separated for readability
class PeerDiscoveryHandler():

    def __init__(self, node):
        self.socket_communication = node

    def start(self):
        status_thread = threading.Thread(target=self.status, args=())
        status_thread.start()
        discovery_thread = threading.Thread(target=self.discovery, args=())
        discovery_thread.start()

    # Prints out all current node connections ever 10 seconds
    def status(self):
        while True:
            print("Current Connections: ")
            for peer in self.socket_communication.peers:
                print(str(peer.ip) + ":" + str(peer.port))
            time.sleep(10)

    # Sends a broadcast message into the network so other nodes can see which connections this node has
    def discovery(self):
        while True:
            handshake_message = self.handshake_message()
            self.socket_communication.broadcast(handshake_message)
            time.sleep(10)

    # An exchange of information between nodes
    def handshake(self, connect_node):
        handshake_message = self.handshake_message()
        self.socket_communication.send(connect_node, handshake_message)

    # Sends the data of the known connected nodes to the node that would like to connect
    def handshake_message(self):
        own_connector = self.socket_communication.socket_connector
        own_peers = self.socket_communication.peers
        data = own_peers
        message_type = "DISCOVERY"
        message = Message(own_connector, message_type, data)
        # Returns the encoded handshake message
        return BlockchainUtils.encode(message)

    def handle_message(self, message):
        # Check if we are already a peer to the message sender
        peers_socket_connector = message.sender_connector
        peers_peer_list = message.data
        new_peer = True
        for peer in self.socket_communication.peers:
            # If the peer already exists in the list, then it is not a new peer
            if peer.equals(peers_socket_connector):
                new_peer = False
        if new_peer:
            self.socket_communication.peers.append(peers_socket_connector)

        # Check if there are new peers in the peers_peer_list that the node should connect to
        for peers_peer in peers_peer_list:
            known_peer = False
            for peer in self.socket_communication.peers:
                if peer.equals(peers_peer):
                    # The peer already exists
                    known_peer = True
            if not known_peer and not peers_peer.equals(self.socket_communication.socket_connector):
                self.socket_communication.connect_with_node(
                    peers_peer.ip, peers_peer.port)
