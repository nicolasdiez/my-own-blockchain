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
import json
import hashlib
import requests
from urllib.parse import urlparse

# this is the sender_public_key when the sender is the blockchain itself, for miner rewarding
MINING_SENDER = "The Blockchain"
# reward for the miner node  is 1 coin
MINING_REWARD = 1
# the number of leading zeros in the hash value to be considered a value nonce
MINING_DIFFICULTY = 2


class Blockchain:

    # constructor
    def __init__(self):

        # attributes (lists)
        self.transactions = []
        self.chain = []  # will contain the list of blocks
        self.nodes = set()  # list of nodes (every node keeps a list with the rest of the nodes available in th network)
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

    # static method cause self was not used at all (method doesn't belong to an instance, belongs to the class itself)
    # Este método lo uso para comprobar que el nonce cumple con los leading zeros del MINING DIFFICULTY
    def valid_proof(self, transactions, last_hash, nonce, difficulty=MINING_DIFFICULTY):
        guess = (str(transactions) + str(last_hash) + str(nonce)).encode('utf8')

        # hash the guess with SHA256 algo
        h = hashlib.new('sha256')
        h.update(guess)
        guess_hash = h.hexdigest()
        # get the first #difficulty characters of the hash and compare them with #difficulty zeros, if equal return True
        return guess_hash[:difficulty] == '0' * difficulty

    def proof_of_work(self):
        # get the last block
        last_block = self.chain[-1]
        # hash the last block
        last_hash = self.hash(last_block)

        # try nonce from 0, until we get a nonce that meet the DIFFICULTY criteria (eg: 2 leading zeros in the hash)
        nonce = 0
        while self.valid_proof(self.transactions, last_hash, nonce) is False:
            nonce += 1

        return nonce

    def hash(self, block):
        # the block dictionary has to be ordered, otherwise inconsistent hashes are obtained
        block_string = json.dumps(block, sort_keys=True).encode('utf8')
        h = hashlib.new('sha256')
        h.update(block_string)
        return h.hexdigest()

    # verify if a chain is valid or not
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1  # start in 1, because 0 is the genesis block

        while current_index < len(chain):
            block = chain[current_index]

            # 1st check: Validate if previous hash value in the block is actually equal to hash of the previous block
            if block['previous_hash'] != self.hash(last_block):
                return False

            # 2nd check: Validate if the nonce is actually a valid one
            # get all the transactions of the block ordered, excepting the last one because is the reward for the miner
            transactions = block['transactions'][:-1]
            transaction_elements = ['sender_public_key', 'recipient_public_key', 'amount']
            transactions = [OrderedDict((k, transaction[k]) for k in transaction_elements) for transaction in transactions]

            if not self.valid_proof(transactions=transactions,
                                    last_hash=block['previous_hash'],
                                    nonce=block['nonce'],
                                    difficulty=MINING_DIFFICULTY):
                return False

            last_block = block
            current_index += 1

        return True

    # method used to decide which chain is the valid one in case the node is receiving more than 1 different chain
    # from the other nodes of the network
    def resolve_conflicts(self):

        # every node maintains a list with the rest of the nodes available in the network (that list is in self.nodes)
        neighbours = self.nodes
        new_chain = None

        # length of the existing chain in the node
        self_node_chain_length = len(self.chain)

        for node in neighbours:

            # get the latest version of the chain from the neighbour node
            response = requests.get('http://' + node + '/chain')

            if response.status_code == 200:
                neighbour_node_chain_length = response.json()['length']
                neighbour_chain = response.json()['chain']

                # if the neighbour node has a longer chain than the self node chain, and his chain is valid, then
                # the self node has to replace his chain
                if neighbour_node_chain_length > self_node_chain_length and self.valid_chain(neighbour_chain):
                    self_node_chain_length = neighbour_node_chain_length
                    new_chain = neighbour_chain

        # new_chain holds the longest valid chain among all the neighbour nodes
        # then update my self chain with the new_chain
        if new_chain:
            self.chain = new_chain
            return True

        return False

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

    def register_node(self, node_url):
        # check if the URL is correct by using the urlparse lib
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')



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


# 5th endpoint -> Return the chain composed of blocks, each block can contain 1 or more transactions
@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


# 6th endpoint -> Return the list of nodes
@app.route('/nodes/get', methods=['GET'])
def get_nodes():
    nodes = list(blockchain.nodes)
    response = {'nodes': nodes}
    return jsonify(response), 200


# 7th endpoint -> Create a new node in the network
@app.route('/nodes/register', methods=['POST'])
def register_node():
    #get the details to create the node from the form in the frontend
    values = request.form
    # split the list of nodes introduced by the user in the UI finding the separator coma (,), also remove spaces
    # example: 127.0.0.1:5002, 127.0.0.1:5003, 127.0.0.1:5004
    nodes = values.get('nodes').replace(' ', '').split(',')

    if nodes is None:
        return 'Error: Please introduce a valid list of nodes', 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'Nodes have been added to the network',
        'total_nodes': [node for node in blockchain.nodes]
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
