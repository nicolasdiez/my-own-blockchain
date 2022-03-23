# Author: nicolas.diez.risueno@gmail.com
# Project: My Own Blockchain

from flask import Flask, request, jsonify, render_template
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
import binascii
from collections import OrderedDict
from Crypto.Signature import PKCS1_v1_5  # Crypto package, Signature class
from Crypto.Hash import SHA


class Transaction:

    # constructor
    def __init__(self, sender_public_key, sender_private_key, recipient_public_key, amount):

        # attributes
        self.sender_public_key = sender_public_key
        self.sender_private_key = sender_private_key
        self.recipient_public_key = recipient_public_key
        self.amount = amount

    # methods
    def to_dictionary(self):
        # OrderedDict used to convert to dictionary
        return OrderedDict({
            'sender_public_key': self.sender_public_key,
            'sender_private_key': self.sender_private_key,
            'recipient_public_key': self.recipient_public_key,
            'amount': self.amount,
        })

    def sign_transaction(self):
        # sender_private_key is used to sign the transaction
        # we have to undo what we did when generating the private_key in the method new_wallet() -> RSA and Hex
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        # we create the signer object from the private_key, with this signer we will sign
        signer = PKCS1_v1_5.new(private_key)
        # hash of the transaction
        hash = SHA.new(str(self.to_dictionary()).encode('utf8'))
        # now we have to sign the hash with the signer object, and we obtain the signature itself
        signature = binascii.hexlify(signer.sign(hash)).decode('ascii')
        return signature


# Create web server
# instantiate the Node
app = Flask(__name__)


# first endpoint -> index
@app.route('/')
def index():
    return render_template('./index.html')


# 2nd endpoint -> make a transaction
@app.route('/make/transaction')
def make_transaction():
    return render_template('./make_transaction.html')


# 3rd endpoint -> view transactions
@app.route('/view/transactions')
def view_transactions():
    return render_template('./view_transactions.html')


# 4th endpoint -> create wallet
@app.route('/wallet/new')
def new_wallet():
    # using lib PyCryptoDome for encryption ($ pip install pycryptodome)
    random_gen = Crypto.Random.new().read
    # use the RSA algorith to generate the private key
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()

    # the private and public key need to be sent to the frontend in the response
    response = {
        # hexlify, from binascii, used to convert to HEX
        # export_key(), from Crypto, used to serialize the key object
        # for further info on the RSA encryption or the private/public objects -> https://pycryptodome.readthedocs.io
        'private_key': binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'),
        'public_key': binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')
    }
    return jsonify(response), 200


# 5th endpoint -> generate transaction
@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    # 'request' module imported from flask package
    sender_public_key = request.form['sender_public_key']
    sender_private_key = request.form['sender_private_key']
    recipient_public_key = request.form['recipient_public_key']
    amount = request.form['amount']

    transaction = Transaction(sender_public_key, sender_private_key, recipient_public_key, amount)

    response = {'transaction': transaction.to_dictionary(),
                'signature': transaction.sign_transaction()}

    return jsonify(response), 200


# run the Flask web server
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)