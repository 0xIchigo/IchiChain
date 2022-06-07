from Crypto.Hash import SHA256
import json
# For serializing and deserializing complex objects to and from JSON
import jsonpickle


class BlockchainUtils():
    @staticmethod
    def hash(data):
        # Creating a string representation of the JSON object
        data_string = json.dumps(data)
        # Converting to a bytes representation
        data_bytes = data_string.encode('utf-8')
        # Hasing the data and returning it
        return SHA256.new(data_bytes)

    # For sending object messages via P2P connection, and the API
    @staticmethod
    def encode(object_to_encode):
        return jsonpickle.encode(object_to_encode, unpicklable=True)

    # Returns the decoded object
    @staticmethod
    def decode(encoded_object):
        return jsonpickle.decode(encoded_object)
