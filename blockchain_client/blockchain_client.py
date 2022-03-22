# Author: nicolas.diez.risueno@gmail.com
# Project: My Own Blockchain

from flask import Flask, jsonify, render_template
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
import binascii


class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value):

        # attributes
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.value = value


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
    return 'Done!!'


# run the Flask web server
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)