from transaction_data import TransactionData 
import time
from hashlib import sha256

# Testowo, nie wiem czy dobrze
# https://www.geeksforgeeks.org/implementing-the-proof-of-work-algorithm-in-python-for-blockchain-mining/

class BlockchainBlock():
    # Constructor
    def __init__(self, previous_hash:str = None, transactions: [] = [], index: int = 0):

        # Header
        self.index = index
        self.nonce = 0
        self.timestamp = time.time()
        self.previous_hash = previous_hash

        # Body
        self.transactions = transactions

        # Hash
        self.hash = self.generate_hash()

    
    def get_block_as_dict(self):
        # self to dict
        return({ 'index': self.index, 'nonce': self.nonce, 'transactions': self.transactions,
                 'timestamp': self.timestamp, 'previous_hash': self.previous_hash, 'hash': self.hash})
    
    def __get_dict_to_hash(self):
        # self to dict
        return({ 'nonce': self.nonce, 'transactions': self.transactions,
                 'timestamp': self.timestamp, 'previous_hash': self.previous_hash})

    def generate_hash(self):
        # sha256 hash of the block dict
        encoded = sha256(str(self.__get_dict_to_hash()).encode('utf-8')).hexdigest()
        return(encoded)
    
    def get_hash(self):
        return(self.hash)
    
    def mine_block(self,difficulty):
        while(self.hash[0:difficulty] != '0'*difficulty):
            self.nonce += 1
            self.hash = self.generate_hash()
    
        

    

    