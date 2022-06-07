from lot import Lot
from blockchain_utils import BlockchainUtils

# TLDR; Proof of Stake is a type of consensus mechanism used to validate cryptocurrency transactions wherein
# validators are selected to propagate the next block  to the blockchain in proportion to their quantity of holdings
# in the associated cryptocurrency


class ProofOfStake():

    def __init__(self):
        # Mapping between an account and its corresponding amount of stake
        self.stakers = {}
        self.set_genesis_node_stake()

    # You need a single staker to solve the block/staker conundrum:
    # How are you going to produce a new block if there isn't anyone staking
    # And if there isn't anyone staking, how are you going to add new stakers
    def set_genesis_node_stake(self):
        genesis_public_key = open("keys/genesisPublicKey.pem", "r").read()
        self.stakers[genesis_public_key] = 1

    # Updates the dictionary based on a person's stake (1 lot per stake)
    def update(self, public_key_string, stake):
        if public_key_string in self.stakers.keys():
            self.stakers[public_key_string] += stake
        else:
            self.stakers[public_key_string] = stake

    # Checks if the public key string is already in the blockchain state
    def get(self, public_key_string):
        if public_key_string in self.stakers.keys():
            return self.stakers[public_key_string]
        else:
            return None

    # Returns all possible lots for a validator
    def validator_lots(self, seed):
        lots = []
        for validator in self.stakers.keys():
            # Enumeration based on the number of tokens staked
            for stake in range(self.get(validator)):
                lots.append(Lot(validator, stake + 1, seed))
        return lots

    # Returns the winning lot thats hash is closest to the chosen hash
    def winner_lot(self, lots, seed):
        winner_lot = None
        least_offset = None
        reference_hash_int_value = int(
            BlockchainUtils.hash(seed).hexdigest(), 16)
        for lot in lots:
            lot_int_value = int(lot.lot_hash(), 16)
            offset = abs(lot_int_value - reference_hash_int_value)
            if least_offset is None or offset < least_offset:
                least_offset = offset
                winner_lot = lot
        return winner_lot

    # Selects the forger
    def forger(self, prev_block_hash):
        lots = self.validator_lots(prev_block_hash)
        winning_lot = self.winner_lot(lots, prev_block_hash)
        return winning_lot.public_key
