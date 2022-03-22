from flask import Flask, render_template
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA


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
@app.route("/")
def index():
    return render_template('./index.html')


# 2nd endpoint -> make a transaction
@app.route("/make/transaction")
def make_transaction():
    return render_template('./make_transaction.html')


# 3rd endpoint -> view transactions
@app.route("/view/transactions")
def view_transactions():
    return render_template('./view_transactions.html')


# 4th endpoint -> create wallet
@app.route("/wallet/new")
def new_wallet():
    # using lib pycryptodome for encryption ($ pip install pycryptodome)
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()

    # the private and public key need to be sent to the frontend in the response
    respond = {
        'private_key':
        'public_key':
    }

    return ''


# run the Flask web server
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)