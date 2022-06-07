from Crypto.PublicKey import RSA
# Importing a signature scheme object to generate and validate signatures
from Crypto.Signature import PKCS1_v1_5
from blockchain_utils import BlockchainUtils
from transactions import Transaction
from block import Block


class Wallet():
    def __init__(self):
        # Using 2048 as a modulo for the prime factoralization of the RSA keypair
        self.key_pair = RSA.generate(2048)

    # Read in a specified key pair
    def from_key(self, file):
        key = ""
        with open(file, "r") as key_file:
            key = RSA.importKey(key_file.read())
        self.key_pair = key

    def sign(self, data):
        data_hash = BlockchainUtils.hash(data)
        signature_scheme_object = PKCS1_v1_5.new(self.key_pair)
        signature = signature_scheme_object.sign(data_hash)
        return signature.hex()

    # This method is static so we can validate signatures without creating a wallet instance
    @staticmethod
    def signature_valid(data, signature, public_key_string):
        signature = bytes.fromhex(signature)
        data_hash = BlockchainUtils.hash(data)
        public_key = RSA.importKey(public_key_string)
        signature_scheme_object = PKCS1_v1_5.new(public_key)
        # Returns if the signature corresponds to the data hash based on the public key
        return signature_scheme_object.verify(data_hash, signature)

    # Returns a string representation of the public key
    def public_key_string(self):
        return self.key_pair.publickey().exportKey("PEM").decode("utf-8")

    # Returns a signed transaction
    def create_transaction(self, receiver, amount, type):
        transaction = Transaction(
            self.public_key_string(), receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction

    # Returns a signed block
    def create_block(self, transactions, lastHash, blockCount):
        block = Block(transactions, lastHash,
                      self.public_key_string(), blockCount)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block
