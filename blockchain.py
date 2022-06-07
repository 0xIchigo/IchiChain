from block import Block
from blockchain_utils import BlockchainUtils
from account_model import AccountModel
from proof_of_stake import ProofOfStake
import time

# TLDR; A blockchain is a distributed, often (and in 99% of most cases should always) decentralized, immutable
# ledger that exists across a network of nodes. This distributed database differs from traditional
# databases such that information is collected in groups, known as blocks, which hold sets of information


class Blockchain():

    def __init__(self):
        self.blocks = [Block.genesis()]
        self.account_model = AccountModel()
        self.pos = ProofOfStake()

    # Adds a block to the blockchain
    def add_block(self, block):
        # Executes all transactions in the block before it is added to the blockchain
        self.execute_transactions(block.transactions)
        if self.blocks[-1].block_count < block.block_count:
            self.blocks.append(block)

    # Creates a human-readable form of the blocks in the blockchain
    def to_json(self):
        data = {}
        json_blocks = []
        for block in self.blocks:
            json_blocks.append(block.to_json())
        data["blocks"] = json_blocks
        return data

    # Returns whether the block count is valid
    def block_count_valid(self, block):
        return self.blocks[-1].block_count == block.block_count - 1

    # Returns whether the last block hash is valid
    def prev_block_hash_valid(self, block):
        latest_blockchain_block_hash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()
        return latest_blockchain_block_hash == block.prev_hash

    # Returns a list of all covered transactions
    def get_covered_transaction_set(self, transactions):
        covered_transactions = []
        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
            else:
                print("The transaction is not covered by the sender")
        return covered_transactions

    # Returns whether transactions have already been covered by the account model
    def transaction_covered(self, transaction):
        if transaction.type != "TRANSACTION":
            return True
        sender_balance = self.account_model.get_balance(
            transaction.sender_public_key)
        return sender_balance >= transaction.amount

    # Takes a list of transactions and updates the account model accordingly
    def execute_transactions(self, transactions):
        for transaction in transactions:
            self.execute_transaction(transaction)

    # Updates the account model by executing the transaction
    def execute_transaction(self, transaction):
        if transaction.type == "STAKE":
            sender = transaction.sender_public_key
            receiver = transaction.receiver_public_key
            # Has to be the same wallet to be a staker - Alice can only stake for herself and not for Bob
            if sender == receiver:
                amount = transaction.amount
                self.pos.update(sender, amount)
                self.account_model.update_balance(sender, -amount)
        else:
            sender = transaction.sender_public_key
            receiver = transaction.receiver_public_key
            amount = transaction.amount
            self.account_model.update_balance(sender, -amount)
            self.account_model.update_balance(receiver, amount)

    # Returns the next forger based on the previous block hash
    def next_forger(self):
        prev_block_hash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()
        return self.pos.forger(prev_block_hash)

    # Returns a newly created block
    def create_block(self, transactions_from_pool, forger_wallet):
        covered_transactions = self.get_covered_transaction_set(
            transactions_from_pool)
        self.execute_transactions(covered_transactions)
        # The new block is produced by the forger's wallet
        new_block = forger_wallet.create_block(covered_transactions, BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest(), len(self.blocks))
        self.blocks.append(new_block)
        # Have to broadcast this new block to the network by returning it to the node - can't just append it
        return new_block

    # Returns if the transaction already exists on the blockchain
    def transaction_exists(self, transaction):
        for block in self.blocks:
            for block_transaction in block.transactions:
                if transaction.equals(block_transaction):
                    return True
        return False

    # Returns if the forger is valid
    def forger_valid(self, block):
        forger_public_key = self.pos.forger(block.prev_hash)
        proposed_block_forger = block.forger
        return forger_public_key == proposed_block_forger

    # Returns that the transactions are valid based on the length of covered txts and txts
    def transaction_valid(self, transactions):
        covered_transactions = self.get_covered_transaction_set(transactions)
        return len(covered_transactions) == len(transactions)

    # Returns whether we are producing a block in the past that would therefore rewrite the blockchain
    def timestamp_valid(self, timestamp):
        return timestamp > self.blocks[-1].timestamp and timestamp < time.time()
