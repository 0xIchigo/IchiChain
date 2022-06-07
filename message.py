# This class is used to send messages to other nodes in the network
class Message():

    def __init__(self, sender_connector, message_type, data):
        # A combination of the IP and port - basically the end point
        self.sender_connector = sender_connector
        self.message_type = message_type
        self.data = data
