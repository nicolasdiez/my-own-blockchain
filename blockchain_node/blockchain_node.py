# Author: nicolas.diez.risueno@gmail.com
# Project: My Own Blockchain

from flask import Flask, jsonify, request, render_template
from time import time
from flask_cors import CORS
from collections import OrderedDict



class Blockchain:

    # constructor
    def __init__(self):

        # attributes (lists)
        self.transactions = []
        self.chain = []  # will contain the list of blocks

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

        # after adding the transactions to the block,
        # we need to reset the current list of transactions
        self.transactions = []
        self.chain.append(block)

    def submit_transaction(self, sender_public_key, recipient_public_key, signature, amount):
        # TODO: reward the miner
        # TODO: validate the signature is correct

        transaction = OrderedDict({
            'sender_public_key': sender_public_key,
            'recipient_public_key': recipient_public_key,
            'signature': signature,
            'amount': amount
        })

        signature_verification = True
        if signature_verification:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        else:
            return False
        return 3



# instantiate the Blockchain
blockchain = Blockchain()

# Create Flask web server
# instantiate the Node
app = Flask(__name__)
CORS(app)   # to overcome CORS blocking requests by Chrome



# 1st endpoint
@app.route("/")
def index():
    return render_template('./index.html')


# 2nd endpoint
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form

    # TODO:  check the required fields

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


# run the Flask web server
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
