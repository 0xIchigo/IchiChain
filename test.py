from proof_of_stake import ProofOfStake
from lot import Lot
import string
import random


# The file I used for testing IchiChain
# This current script makes sure the next forger choice is both randomized and proportionate to one's stake

def get_random_str(length):
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for i in range(length))
    return random_string


if __name__ == '__main__':
    pos = ProofOfStake()
    pos.update("bob", 10)
    pos.update("alice", 100)

    bob_wins = 0
    alice_wins = 0

    for i in range(100):
        forger = pos.forger(get_random_str(i))
        if forger == "bob":
            bob_wins += 1
        elif forger == "alice":
            alice_wins += 1

    print("Bob won: " + str(bob_wins) + " times")
    print("Alice won: " + str(alice_wins) + " times")
