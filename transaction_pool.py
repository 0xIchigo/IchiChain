# This class holds the set of all unconfirmed transactions that have been validated and are ready to be pushed to the blockchain
class TransactionPool():
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    # Returns whether a transaction exists
    def transaction_exists(self, transaction):
        for pool_transaction in self.transactions:
            if pool_transaction.equals(transaction):
                return True
        return False

    # Removes a transaction from the pool so they aren't included in future blocks
    def remove_from_pool(self, transactions):
        new_pool_transactions = []
        for pool_transaction in self.transactions:
            insert = True
            for transaction in transactions:
                if pool_transaction.equals(transaction):
                    # Wont insert the transaction in the new list if it already exists
                    insert = False
                if insert == True:
                    new_pool_transactions.append(pool_transaction)
        self.transactions = new_pool_transactions

    # Triggering the forger selection process if the threshhold of pooled transactions is reached
    # and the production of a new block is required
    def forger_required(self):
        # For simplicity, we are generating 1 block per 3 transactions
        if len(self.transactions) >= 3:
            return True
        else:
            return False
