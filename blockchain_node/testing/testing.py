# -----------------------------------------------------------------------------------------------
# --------------------------------- TESTING SOME FUNCTIONALITIES --------------------------------
# -----------------------------------------------------------------------------------------------


def proof_of_stake(self):
        # get the last block
        last_block = self.chain[-1]
        # hash the last block
        last_hash = self.hash(last_block)
        # try nonce from 0, until we get a nonce that meet the DIFFICULTY criteria (eg: 2 leading zeros in the hash)
        nonce = 0
        while self.valid_proof(self.transactions, last_hash, nonce) is False:
            nonce += 1
        return nonce


def mine_2():
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


def resolve_conflicts_2(self):

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


def register_node_2(self, node_url):
        self.nodes.add(node_url)

        # check if the URL is correct by using the urlparse lib
        parsed_url = urlparse(node_url)
        if parsed_url.scheme:
            self.nodes.add(parsed_url.scheme)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


def submit_transaction_2(self, sender_public_key, recipient_public_key, signature, amount):

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


def valid_chain_2(self, chain):
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


def verify_transaction_signature_2(self, sender_public_key, signature, transaction):
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new(str(transaction).encode('utf8'))
        # return TRUE if the 'h' (hash) corresponds to the 'signature'
        try:
            verifier.verify(h, binascii.unhexlify(signature))
            return True
        except ValueError:
            return False


def proof_of_stake_2(self):
    # get the last block
    last_block = self.chain[-1]
    # hash the last block
    last_hash = self.hash(last_block)
    # try nonce from 0, until we get a nonce that meet the DIFFICULTY criteria (eg: 2 leading zeros in the hash)
    nonce = 0
    while self.valid_proof(self.transactions, last_hash, nonce) is False:
        nonce += 1
    return nonce


def submit_transaction_3(self, sender_public_key, recipient_public_key, signature, amount):

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


def valid_chain_3(self, chain):
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


def submit_transaction_4 (self, sender_public_key, recipient_public_key, signature, amount):

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


def valid_chain_4(self, chain):
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


def resolve_conflicts_3(self):

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


def register_node_3(self, node_url):
        self.nodes.add(node_url)

        # check if the URL is correct by using the urlparse lib
        parsed_url = urlparse(node_url)
        if parsed_url.scheme:
            self.nodes.add(parsed_url.scheme)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


def submit_transaction_3(self, sender_public_key, recipient_public_key, signature, amount):

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


def valid_chain_3(self, chain):
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


def verify_transaction_signature_3(self, sender_public_key, signature, transaction):
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new(str(transaction).encode('utf8'))
        # return TRUE if the 'h' (hash) corresponds to the 'signature'
        try:
            verifier.verify(h, binascii.unhexlify(signature))
            return True
        except ValueError:
            return False


def proof_of_stake_3(self):
    # get the last block
    last_block = self.chain[-1]
    # hash the last block
    last_hash = self.hash(last_block)
    # try nonce from 0, until we get a nonce that meet the DIFFICULTY criteria (eg: 2 leading zeros in the hash)
    nonce = 0
    while self.valid_proof(self.transactions, last_hash, nonce) is False:
        nonce += 1
    return nonce


def submit_transaction_4(self, sender_public_key, recipient_public_key, signature, amount):

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


def valid_chain_4(self, chain):
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


def submit_transaction_5 (self, sender_public_key, recipient_public_key, signature, amount):

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


def valid_chain_5(self, chain):
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