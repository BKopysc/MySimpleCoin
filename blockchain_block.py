from transaction_data import TransactionData 
import time
from hashlib import sha256

# Testowo, nie wiem czy dobrze
# https://www.geeksforgeeks.org/implementing-the-proof-of-work-algorithm-in-python-for-blockchain-mining/

class BlockchainBlock(object):
    # Constructor
    def __init__(self, previous_hash:str = None, transactions: [] = []):
        self.version = 1
        self.nonce = 0
        #self.difficulty = 1
        self.transactions = transactions
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.hash = self.__generate_hash()
    
    def get_block_as_dict(self):
        # self to dict
        return({ 'version': self.version, 'nonce': self.nonce, 'transactions': self.transactions,
                 'timestamp': self.timestamp, 'previous_hash': self.previous_hash})

    def __generate_hash(self):
        # sha256 hash of the block dict
        encoded = sha256(str(self.get_block_as_dict()).encode('utf-8')).hexdigest()
        return(encoded)
    
        

    

    