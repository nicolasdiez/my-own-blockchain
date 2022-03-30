# Author: nicolas.diez.risueno@gmail.com
# Project: My Own Blockchain
# File description:
# Each Node in the blockchain will have a set of transactions sent by the users/clients (Alice or Bob).
# The Node holds several transactions sent by different users.
# When the Node success in mining the block, then the block is added to the blockchain.

from flask import Flask, request, jsonify, render_template
from time import time
from flask_cors import CORS
from collections import OrderedDict
import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from uuid import uuid4

# this is the sender_public_key when the sender is the blockchain itself, for miner rewarding
MINING_SENDER = "The Blockchain"
# reward for the miner node  is 1 coin
MINING_REWARD = 1

class Blockchain:

    # constructor
    def __init__(self):

        # attributes (lists)
        self.transactions = []
        self.chain = []  # will contain the list of blocks
        self.node_id = str(uuid4()).replace('-', '')  # every time a node is created it has its own ID

        # methods
        # create the genesis block
        self.create_block(0, '00')

    # methods
    def create_block(self, nonce, previous_hash):
        """
        Add a block of transactions to the chain
        :param nonce:
        :param previous_hash:
        :return:
        """

        # dictionary
        block = {'block_number': len(self.chain) + 1,  # 1st block -> block_number = 1
                 'timestamp': time(),
                 'transactions': self.transactions,
                 'nonce': nonce,
                 'previous_hash': previous_hash}

        # after adding the transactions to the block, the current list of transactions is cleared
        # (in real blockchain, the miner selects some transactions to add to the block, not all of them)
        self.transactions = []
        self.chain.append(block)
        return block

    def verify_transaction_signature(self, sender_public_key, signature, transaction):
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new(str(transaction).encode('utf8'))
        # return TRUE if the 'h' (hash) corresponds to the 'signature'
        try:
            verifier.verify(h, binascii.unhexlify(signature))
            return True
        except ValueError:
            return False

    def proof_of_work(self):
        return 12345

    def hash(self, block):
        return 'abc'

    def submit_transaction(self, sender_public_key, recipient_public_key, signature, amount):

        transaction = OrderedDict({
            'sender_public_key': sender_public_key,
            'recipient_public_key': recipient_public_key,
            'amount': amount
        })

        # Reward the miner for mining the block (transaction comes from the BC, not from a wallet)
        if sender_public_key == MINING_SENDER:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        else:
            # transaction from wallet to another wallet
            signature_verification = self.verify_transaction_signature(sender_public_key, signature, transaction)
            if signature_verification:
                self.transactions.append(transaction)
                return len(self.chain) + 1
            else:
                return False
            return 3


# instantiate the Blockchain
blockchain = Blockchain()

# Create Flask web server
# instantiate the Node web server
app = Flask(__name__)
CORS(app)   # to overcome CORS blocking requests by Chrome


# 1st endpoint
@app.route("/")
def index():
    return render_template('./index.html')


# 2nd endpoint -> Create a new transaction (add a transaction to the next Block in the blockchain)
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form

    # check if there is any empty or missing value in the input
    required = ['confirmation_sender_public_key', 'confirmation_recipient_public_key', 'transaction_signature', 'confirmation_amount']
    if not all (k in values for k in required):
        return 'Missing values', 400

    # transaction_results will contain the number of the next Block that will contain the Transaction itself
    transaction_results = blockchain.submit_transaction(values['confirmation_sender_public_key'],
                                                        values['confirmation_recipient_public_key'],
                                                        values['transaction_signature'],
                                                        values['confirmation_amount'])
    if transaction_results == False:
        response = {'message': 'Invalid transaction/signature'}
        return jsonify(response), 406
    else:
        response = {'message': 'Transaction will be added to the Block #' + str(transaction_results)}
        return jsonify(response), 201

    response = {'message': 'Ok'}
    return jsonify(response), 201   # returning 201 signaling that we are creating a new resource


# 3rd endpoint -> Get the transactions in the Node
@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = blockchain.transactions
    response = {'transactions': transactions}
    return jsonify(response), 200


# 4th endpoint -> Mine a block (= find the Nonce number)
@app.route('/mine', methods=['GET'])
def mine():
    # run the proof of work algorithm
    nonce = blockchain.proof_of_work()

    # reward the miner = submit a new transaction to be incorporated into the next block
    blockchain.submit_transaction(sender_public_key = MINING_SENDER,
                                  recipient_public_key = blockchain.node_id,
                                  signature = '',   # when rewarding the miner, there is no signature
                                  amount = MINING_REWARD)

    last_block = blockchain.chain[-1]  # get the last block of the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(nonce = nonce, previous_hash = previous_hash)

    response = {
        'message': 'New block created',
        'block_number': block['block_number'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# run the Flask web server
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
