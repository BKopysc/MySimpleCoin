from transaction_data import TransactionData 
import time
from hashlib import sha256

class BlockchainBlock():
    # Constructor
    def __init__(self, previous_hash:str = None, transactions: [] = [], index: int = 0):

        # Header
        self.nonce = 0
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.minerId = ""

        # Body
        self.transactions: list[TransactionData] = transactions

        # Hash
        self.hash = ""

    
    def get_block_as_dict(self):
        # self to dict
        block_dict = { 'nonce': self.nonce, 'transactions': [],
                 'timestamp': self.timestamp, 'previous_hash': self.previous_hash, 'hash': self.hash, 'minerId': self.minerId}
        for transaction in self.transactions:
            block_dict["transactions"].append(transaction.get_transaction_data_as_dict())
        return(block_dict)
    
    def __get_dict_to_hash(self):
        # self to dict
        return({ 'nonce': self.nonce, 'transactions': self.transactions, 'previous_hash': self.previous_hash, 'minerId': self.minerId})

    def generate_hash(self):
        # sha256 hash of the block dict
        encoded = sha256(str(self.__get_dict_to_hash()).encode('utf-8')).hexdigest()
        return(encoded)
    
    def gen_set_hash(self):
        self.hash = self.generate_hash()
    
    def get_hash(self):
        return(self.hash)
    
    def mine_block(self,difficulty, minerId):
        self.minerId = minerId
        while(self.hash[0:difficulty] != '0'*difficulty):
            self.nonce += 1
            self.hash = self.generate_hash()
        self.timestamp = time.time()

    def update_and_get_coinbase_transaction(self, miner_name):
        for transaction in self.transactions:
            if(transaction.is_coinbase == True):
                return transaction.update_and_get_coinbase_transaction(miner_name)
        return None

    def load_all_from_dict(self, block_dict):
        self.nonce = block_dict["nonce"]
        self.timestamp = block_dict["timestamp"]
        self.previous_hash = block_dict["previous_hash"]
        self.hash = block_dict["hash"]
        self.minerId = block_dict["minerId"]
        self.transactions = []
        for transaction_dict in block_dict["transactions"]:
            transaction = TransactionData()
            transaction.load_all_from_dict(transaction_dict)
            self.transactions.append(transaction)
    
        

    

    