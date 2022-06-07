import time
import copy

# TLDR; Blocks are data structures within a blockchain that record and hold
# information permanetly in the form of a ledger. The information within these blocks must
# be verified by the network (via validators) before they are closed and a new block is created


class Block():

    def __init__(self, transactions, prev_hash, forger, block_count):
        self.block_count = block_count
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.timestamp = time.time()
        # The forger is the node that creates the next block
        self.forger = forger
        self.signature = ''

    # Creates IchiChain's genesis block
    @staticmethod
    def genesis():
        genesis_block = Block([], "genesis hash", "genesis", 0)
        # Overrides the timestamp to 0 so the genesis block is the same for all new nodes and circumvents certain future validation errors
        genesis_block.timestamp = 0
        return genesis_block

    def to_json(self):
        data = {}
        data["block_count"] = self.block_count
        data["prev_hash"] = self.prev_hash
        data["signature"] = self.signature
        data["forger"] = self.forger
        data["timestamp"] = self.timestamp
        json_transactions = []

        # Iterates over transactions so we can see them in a human-readable form; can't just return self.__dict__ in this case
        for transaction in self.transactions:
            json_transactions.append(transaction.to_json())

        data["transactions"] = json_transactions
        return data

    # Makes a copy of the JSON representation so we can use it without altering the real object
    def payload(self):
        json_representation = copy.deepcopy(self.to_json())
        json_representation["signature"] = ''
        return json_representation

    # All blocks must be signed in order for them to be validated
    def sign(self, signature):
        self.signature = signature
