import time
import uuid
import os
from dotenv import load_dotenv
import copy
from key_util import KeyUtil 

load_dotenv()
BLOCK_REWARD = float(os.getenv("BLOCK_REWARD"))
TRANS_FEE = float(os.getenv("FEE_PERCENT"))
key_util = KeyUtil()

class TransactionData:
    def __init__(self, sender_name: str = "", receiver_name:str = "" , amount: float = 0, 
                 timestamp: float = None, is_coinbase: bool = False, fees: float = 0, sender_private_key = None):
        self.id: int = uuid.uuid4().int
        self.is_coinbase: bool = is_coinbase
        self.sender_name = sender_name
        self.receiver_name = receiver_name
        self.amount = amount * (1-TRANS_FEE)
        self.verified = False #local
        self.signature = ""

        if(fees == 0):
            self.fees = amount * TRANS_FEE
        else:
            self.fees = fees
        if(timestamp == None):
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp

        if(is_coinbase == True):
            self.__set_coinbase_transaction()

        if(sender_private_key != None):
            self.signature = key_util.sign(sender_private_key, self.get_transaction_data_as_str())

    def set_id(self, id):
        self.id = id

    def verify_signature(self, sender_public_key):
        return key_util.verify(sender_public_key, self.signature, self.get_transaction_data_as_str())

    def get_transaction_data_as_dict(self):
        return({"sender_name": self.sender_name, 
                "receiver_name": self.receiver_name, 
                "amount": self.amount, 
                "is_coinbase": self.is_coinbase,
                "fees": self.fees,
                "id": self.id,
                "timestamp": self.timestamp,
                "signature": self.signature})
    
    def load_all_from_dict(self, transaction_dict):
        self.sender_name = transaction_dict["sender_name"]
        self.receiver_name = transaction_dict["receiver_name"]
        self.amount = transaction_dict["amount"]
        self.is_coinbase = transaction_dict["is_coinbase"]
        self.timestamp = transaction_dict["timestamp"]
        self.fees = transaction_dict["fees"]
        self.id = transaction_dict["id"]
        self.signature = transaction_dict["signature"]
    
    def __set_coinbase_transaction(self):
        self.is_coinbase = True
        self.sender_name = "network_coinbase"
        self.receiver_name = None
        self.amount = (self.fees + BLOCK_REWARD)
        self.fees = 0
        self.timestamp = time.time()

    def update_and_get_coinbase_transaction(self, miner_name):
        self.receiver_name = miner_name
        #self.is_coinbase = False
        coinbase_copy = copy.deepcopy(self)
        coinbase_copy.is_coinbase = False
        coinbase_copy.amount = (self.fees + BLOCK_REWARD) * (1- TRANS_FEE)
        coinbase_copy.fees = coinbase_copy.amount * TRANS_FEE
        return coinbase_copy


    def get_transaction_data_as_str(self):
        #dict to str
        return(str(self.get_transaction_data_as_dict()))

    

    