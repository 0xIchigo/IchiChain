# This class saves the IP and port of a connection
class SocketConnector():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    # Checks whether a connector equals to another
    def equals(self, connector):
        return connector.ip == self.ip and connector.port == self.port
