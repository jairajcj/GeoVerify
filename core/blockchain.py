import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': [] # List of verified assets
        }
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def add_verification(self, verification_data):
        """Adds a verification record to the current block (or a buffer)"""
        # For simplicity in this efficiency demo, we add to the last block or create new one on demand
        # Here we'll just return the data structure to be added to a new block mining simulation
        return verification_data

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_block = block
            block_index += 1
        return True
