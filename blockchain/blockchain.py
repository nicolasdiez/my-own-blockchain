from flask import Flask, render_template
from time import time


class Blockchain:

    # constructor
    def __init__(self):

        # attributes (lists)
        self.transactions = []
        self.chain = []  # will contain the list of blocks

        # methods
        # create the genesis block
        self.create_block(0, '00')

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


# instantiate the Blockchain
blockchain = Blockchain()

# Create Flask web server
# instantiate the Node
app = Flask(__name__)


# first endpoint
@app.route("/")
def index():
    return render_template('./index.html')


# run the Flask web server
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help="port to listen to")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
