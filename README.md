# my_own_blockchain
Miniaturized blockchain model implementing PoW consensus. Architecture consist of two types of elements: Nodes and Clients.

# My Own Blockchain

- Author: nicolas.diez.risueno@gmail.com
- Project: My Own Blockchain

Summary:
- This project is a miniaturized blockchain model created by Nicolas Díez
- The architecture consist of two types of elements: Nodes and Clients

Considerations:
- The public key of the sender/recipient is used as their crypto wallet address
- Proof-of-Work is used as consensus mechanism (based on Bitcoin)
- When blockchain conflicts arise among nodes, the longest valid chain is chosen as legit blockchain
- Miner is rewarded with MINING_REWARD coins
- The mining difficulty is set as MINING_DIFFICULTY leading zeros in the hashed number
- SHA256 is used as secure hashing algorithm
- You can check the file "blockchain network example with 3 nodes and 2 clients.JPG" to get an idea of a possible blockchain network architecture that you can implement with this Project

-------------

# How to run the Node web server

- Open PyCharm terminal (or any other cli)
- Go to the blockchain_node directory ($ cd D:\PycharmProjects\blockchain_nico\blockchain_node)
- Run file "blockchain_node.py" with the following arguments: -p PORT_NUMBER (eg: python blockchain_node.py -p 5003)
- Now a blockchain network Node is running on: http://127.0.0.1:5003/ 

- You can run as many Nodes as you want by changing the PORTNUMBER (eg: python blockchain_node.py -p 5004, python blockchain_node.py -p 5005, ...)

- You can check the file "blockchain node UI.JPG" to get an idea of the node UI

-------------

# How to run the Client web server 

- Open PyCharm terminal (or any other cli)
- Go to the blockchain_client directory ($ cd D:\PycharmProjects\blockchain_nico\blockchain_client)
- Run file "blockchain_client.py" with the following arguments: -p PORT_NUMBER (eg: python blockchain_client.py -p 8081)
- Now a blockchain Client is running on: http://127.0.0.1:8081/ 

- You can run as many Clients as you want by changing the PORTNUMBER (eg: python blockchain_client.py -p 8082, python blockchain_client.py -p 8083, ...)

- You can check the file "blockchain client UI.JPG" to get an idea of the client UI

-------------

# Description of the Node UI functionalities

- Home -> Transactions to be added to the next block: Here you can see the transactions that the Clients (= users) have sent to the Node. Transactions consist of a transfer of coins ("amount") between the "Sender Public Key" and the "Recipient Public Key". Transactions have to be signed with the "Sender Private Key" 

- Home -> Mine: This button mines the next block with all the transactions shown on the table labelled as "Transactions to be added to the next block". As a reminder, mining a block means to find a "nonce" number which produces a SHA-256 hash number with leading zeros equal to MINING_DIFFICULTY.

- Home -> Transactions on the Blockchain: Here you can see all the blocks that contain the local copy of the Node chain, along with all the transactions they contain.

- Configure Nodes -> Add Blockchain nodes: Here you can add the IP of the other Nodes of the network, so the current instance of the Node is aware of them. When a Node is aware of other nodes in the network, a consensus mechanism among them have to be applied everytime a new block is added to the blockchain.

- Configure Nodes -> This node can retrieve Blockchain data from the following nodes: Here you can see the IP list of all the nodes that the current instance of the Node is aware of.

-------------

# Description of the Client UI functionalities

- Wallet Generator: Here you can generate a pair of public and private keys to be used as a wallet. The public key is used as wallet address to send/receive coins to/from other wallets. The private key is used to sign every transaction. Remember that, a transaction is a transfer of a certain amount of coins, which is sent from the sender´s public key to the recipient´s public key, and is signed with the sender´s private key.

- Make Transaction: Here you can send an amount of coins from the a sender´s public key to a recipient´s public key. The transaction must be signed with the sender´s private key. When generating a transaction, you have to choose to which node you want to send the transaction to, in order for the node to mine the next block which includes your new submitted transaction.

- View Transactions: By submitting the IP of a node, here you can see all the transactions contained on the local copy of the node.






