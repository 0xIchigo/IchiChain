import uuid
import time
import copy


class Transaction():
    def __init__(self, sender_public_key, receiver_public_key, amount, type):
        # Sender's address
        self.sender_public_key = sender_public_key
        # Receiver's address
        self.receiver_public_key = receiver_public_key
        self.amount = amount
        self.type = type
        # UUID generates random objects of 128 bits as ids. We use hex to get a 32-character lowercase hexadecimal string
        self.id = (uuid.uuid1()).hex
        self.timestamp = time.time()
        self.signature = ''

    # So we can see the transaction object in a human-readable form - a dictionary
    def to_json(self):
        return self.__dict__

    def sign(self, signature):
        self.signature = signature

    # Returns a copy of the JSON representation so we can use it without altering the real object
    def payload(self):
        json_representation = copy.deepcopy(self.to_json())
        json_representation['signature'] = ''
        return json_representation

    # Returns if the transaction is equal to an existing transaction
    def equals(self, transaction):
        return self.id == transaction.id
