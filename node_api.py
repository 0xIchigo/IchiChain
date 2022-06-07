from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from blockchain_utils import BlockchainUtils

node = None


# FlaskView allows us to create endpoints which we can call for HTTP requests


class NodeAPI(FlaskView):

    def __init__(self):
        # Creating a Flask application allows us to interact with route endpoints
        self.app = Flask(__name__)

    def start(self, api_port):
        # Subclassing Flask with NodeAPI. Route base defines the entry point
        NodeAPI.register(self.app, route_base="/")
        self.app.run(host="localhost", port=api_port)

    # Injects the node object into the NodeAPI
    def inject_node(self, injected_node):
        # Architectural limitations concerning Flask requires us to us a global node
        global node
        node = injected_node

    @route("/info", methods=["GET"])
    def info(self):
        return "This is a communication interface for IchiChain, a rudimentary Proof of Stake blockchain coded in Python by 0xIchigo", 200

    # Endpoint for our blockchain via the JSON representation
    @route("/blockchain", methods=["GET"])
    def blockchain(self):
        return node.blockchain.to_json(), 200

    # Endpoint for the transaction pool
    @route("/transactionPool", methods=["GET"])
    def transaction_pool(self):
        transactions = {}
        # Enumeration so we can get back i, the counter for our index, which allows us to index the dictionary
        for i, transaction in enumerate(node.transaction_pool.transactions):
            transactions[i] = transaction.to_json()
            # Converting input to a JSON representation
        return jsonify(transactions), 200

    # POST request for single transactions
    @route("/transaction", methods=["POST"])
    def transaction(self):
        values = request.get_json()
        if not "transaction" in values:
            return "Missing transaction value", 400
        transaction = BlockchainUtils.decode(values["transaction"])
        # Handles the transaction
        node.handle_transaction(transaction)
        # Generates a response
        response = {"message": "Received transaction"}
        return jsonify(response), 201
