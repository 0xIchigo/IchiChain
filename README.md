# IchiChain
IchiChain is a rudimentary Proof of Stake blockchain coded in Python by 0xIchigo. The purpose of this project was to deepen my understanding of how blockchains and consensus mechanisms operate on a more technical, fundamental level. I have open-sourced the code in an effort to provide educational value to those looking to deepen their understanding of blockchain technology as well as those looking to code their own blockchains!

The following will be a high-level overview regarding blockchains, proof of stake, and how to use IchiChain

# What is a blockchain?
A blockchain is a distributed, immutable, decentralized, peer-to-peer ledger that exists across a network of nodes. This distributed database differs from traditional databases such that it provides greater privacy, security, and transparency as well as the information collected in the ledger is collected in special groups known as blocks. 

Blocks are data structures within a blockchain that record and hold information permanently. The information within these blocks are verified by the network via its validators before they are created and propagated to the blockchain. In order for a block to be validated, it must contain a valid block count, signature, timestamp, previous block hash, and a valid set of transactions.

Public key cryptography (PKC), also known as asymmetric cryptography, helps in this validation process. PKC operates by creating a key pairs  that are mathematically linked using encryption algorithms. One of the most common encryption algorithm, which is also used in IchiChain, is RSA. In RSA, keys are generated using a modulas that is arrived at usually through prime factoralization. 

The public key is used by a sender to encrypt information whereas the private key is used by a recipient to decrypt the information. Since each key pair is unique, we can ensure that data encrypted using a public key can only be decrypted by the corresponding private key. PKC is used throughout IchiChain for hashing data, checking whether a signature corresponds to hashed data based on a given public key, running nodes with a specified key file, sending transactions, and so forth. PKC therefore aids in cryptographically securing and validating data pushed to the blockchain but how does the network agree about which should be, or have already been, pushed?

# What is a consensus algorithm?
In short, a consensus algorithm is a procedure through which all peers on the blockchain network come into agreement regarding the present state of the chain. Consensus algorithms provide reliability as it makes sure every new block added to the network is the only truth agreed upon by all nodes within the network. Because of this, unknown peers are able to trust one another in a distributed computing environment since they all validate data in the same manner.

The most well-known consensus algorithm is Proof of Work (PoW), which was first purported by Hal Finney in 2004 with his idea of "reusable proof of work" via the SHA-256 hashing algorithm. In 2009, Satoshi Nakamoto's Bitcoin became the first widely adopted PoW distributed system. PoW is essentially a cryptographic proof wherein one party (the prover) proves to others (the verifiers) that a specific computational effort has been expended. This is essential since generating hashes is quite trivial. In order to complicate the process and turn it into "work" PoW networks set a target difficulty via setting a "target" for the hash so blocks are "mined" in a predictable amount of time. PoW makes it very difficult to alter any aspect of the blockchain since it would require a monopolization of the network's computing power or re-mining all subsequent blocks and producing a new block with fraudulent transactions. 

The main issue with this is the amount of energy needed to solve the hash and the arms race that follows - network security is relative to energy spent and not the hashrate itself.

# What is Proof of Stake?
Proof of Stake (PoS) is a type of consensus mechanism wherein validators are selected to propagate the next block to the blockchain in proportion to their quantity of holdings in the associated cryptocurrency. Basically, holders of the associated cryptocurrency set aside a number of coins to become stakers, or validators, with their coins as collateral for the chance to randomly validate (or "mine" in the PoW sense) the next block. The validator randomly chosen to produce the next block is often referred to as the forger. 

IchiChain utilizes PoS by employing an Account Model. The Account Model keeps track of all balances as a global state. This state can be understood as a database of all accounts, contract code, private keys, and their current balances of the assets on the network. This differs from Bitcoin's architecture as, instead of having each coin be referenced uniquely, IchiCoins are represented as a balance within an account. 

A lot mechanism is used in order to determine the next forger based on the proportionality of stake distributed amongst stakers. A lot is essentially a unique hash generated based on a staker's public key. Hash chaining is used in order to ensure the selection of the forger is entirely random. The amount of tokens held by the validator determines the amount of lots an account is allowed to create. 

For example: Bob is staking 10 IchiCoins whereas Alice is staking 5 IchiCoins. Bob's account is allowed to create 10 lots for the next block selection whereas Alice's account can only produce 5 due to the proportionality of their stakes. Bob therefore has a higher chance to be selected as the next forger because he has twice Alice's stake. Instead, if Alice had 100 IchiCoins then her chance at becoming the next forger is ten times of that of Bob's.

# Cool primer on blockchain tech, but how do I use IchiChain?
To run an instance of IchiChain: clone the repository, install the associated dependencies (Flask, jsonpickle, and a few others), and at the command line write python main.py (the IP you'd like to run on) (the port) (the REST API port) (optional: a key file)

For testing purposes try running these commands all in separate instances of command prompt:

- python main.py localhost 10001 5000 keys/genesisPrivateKey.pem
- python main.py localhost 10002 5001
- python main.py localhost 10003 5003 keys/stakerPrivateKey.pem
- python interaction.py

The optional key file arg is used in the third instance so we can simulate Alice's computer and test our PoS blockchain by selecting the next forger. You'll notice the first instance also includes an optional key file argument as that instance becomes the genesis node staker. This is done to solve what I refer to as the block/staker conundrum: 

How are you going to produce a new block if there isn't anyone staking? And, if there isn't anyone staking, how are you going to add new stakers which requires a new block?

We therefore provide a single, genesis staker in order to solve this conundrum.

# Further Reading/What's Next
In the future as I learn more React I'd love to update this repo with a nice front-end for IchiChain, however, I am finding myself more interested in back-end and smart contract development so it may be a long time before I revisit this project. A lot of the Proof of Stake mechanism that was implemented can be found in Lukas Hubl's excellent [Udemy Course](https://www.udemy.com/course/build-your-own-proof-of-stake-blockchain/)

If you're interested in learning more about blockchains or building your own, here's a list of useful links:
- [What Is Blockchain Technology?](https://academy.binance.com/en/articles/what-is-blockchain-technology-a-comprehensive-guide-for-beginners)
- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Ethereum Whitepaper](https://ethereum.org/en/whitepaper/)
- [Python Tutorial for Beginners](https://www.youtube.com/watch?v=8124kv-632k&ab_channel=freeCodeCamp.org)
- [How To Build A Blockchain In Python](https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/)
- [Learn Cryptography](https://www.tutorialspoint.com/cryptography/index.htm)
- [Formalizing and Securing Relationships on Public Networks](https://firstmonday.org/ojs/index.php/fm/article/download/548/469)
