from transaction_data import TransactionData 
import time
from hashlib import sha256

# Testowo, nie wiem czy dobrze

class BlockchainBlock(object):
    # Constructor
    def __init__(self, previous_hash:str = None, timestamp: float = None, index = 0, transactions: [] = []):
        self.version = 1
        self.index =1
        self.nonce = 1
        self.difficulty = 1
        self.previous_hash = previous_hash
        self.transactions = transactions
        if(timestamp == None):
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp

    
    def get_block_as_dict(self):
        return({"version": self.version, 
                "nonce": self.nonce, 
                "previous_hash": self.previous_hash, 
                "timestamp": self.timestamp, 
                "transactions": self.transactions})

    def get_hash(self):
        # sha256 hash of the block dict
        encoded = sha256(str(self.get_block_as_dict()).encode('utf-8')).hexdigest()
        return(encoded)
    
        

    

    