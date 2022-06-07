# The account model keeps track of all balances as a global state.
# This state can be understood as a database of all accounts, contract code, private keys,
# and their current balances of the different assets on the network.
# Instead of having each coin be referenced uniquely, as in the case of Bitcoin,
# IchiCoins are represented as a balance within an account

class AccountModel():

    def __init__(self):
        # Holds the public keys of all network participants
        self.accounts = []
        # Saves the mapping between the public key and its corresponding token amount
        self.balances = {}

    # Adds an account so long as the account does not already exist
    def add_account(self, public_key_string):
        if not public_key_string in self.accounts:
            self.accounts.append(public_key_string)
            self.balances[public_key_string] = 0

    # Returns the balance of an account
    def get_balance(self, public_key_string):
        # Incase the account doesn't already exist, we add it to accounts
        if public_key_string not in self.accounts:
            self.add_account(public_key_string)
        return self.balances[public_key_string]

    # Updates the balance of an account
    def update_balance(self, public_key_string, amount):
        if public_key_string not in self.accounts:
            self.add_account(public_key_string)
        self.balances[public_key_string] += amount
