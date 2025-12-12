from flask import Flask, render_template, jsonify, request
from core.blockchain import Blockchain
from core.verifier import GeoSentinel

app = Flask(__name__)

# Initialize Core Components
blockchain = Blockchain()
sentinel = GeoSentinel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/verify', methods=['POST'])
def verify_asset():
    data = request.json
    lat = float(data.get('lat', 0))
    lon = float(data.get('lon', 0))
    
    # 1. AI Verification
    verification_result = sentinel.verify_location(lat, lon)
    
    # 2. Blockchain Recording (Mining)
    # In a real app, this would be more complex. Here we simulate mining a block for this transaction.
    last_block = blockchain.get_last_block()
    proof = last_block['proof'] + 1 # Simplified Proof of Work
    previous_hash = blockchain.hash(last_block)
    
    new_block = blockchain.create_block(proof, previous_hash)
    new_block['data'].append(verification_result) # Add the data to the block
    
    return jsonify({
        "verification": verification_result,
        "block_index": new_block['index'],
        "block_hash": blockchain.hash(new_block)
    })

@app.route('/api/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
