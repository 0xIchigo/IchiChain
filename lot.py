from blockchain_utils import BlockchainUtils

# Using lots to determine the proportionality of stake distributed amongst stakers so we
# can assign the next forger based on this distribution


class Lot():
    # The amount of tokens held determines the amount of lots an account is allowed to create
    # Ex. Bob is staking 10 tokens so he can create 10 lots for the next block selection
    # Alice has 5 tokens so she can only create 5 lots for the next block selection
    # Bob therefore has a higher chance to be selected as the next forger because he has twice Alice's stake

    def __init__(self, public_key, iteration, prev_block_hash):
        self.public_key = str(public_key)
        self.iteration = iteration
        self.prev_block_hash = prev_block_hash

    # The selection of the forger has to be random, which is why we are hash chaining
    def lot_hash(self):
        hash_data = self.public_key + self.prev_block_hash
        # Hash chaining to create different lots
        for _ in range(self.iteration):
            hash_data = BlockchainUtils.hash(hash_data).hexdigest()
        return hash_data
