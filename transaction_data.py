import time
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
BLOCK_REWARD = float(os.getenv("BLOCK_REWARD"))

class TransactionData:
    def __init__(self, sender_name: str = "", receiver_name:str = "" , amount: float = 0, 
                 timestamp: float = None, is_coinbase: bool = False, fees: float = 0):
        self.id: int = uuid.uuid4().int
        self.is_coinbase: bool = is_coinbase
        self.sender_name = sender_name
        self.receiver_name = receiver_name
        self.amount = amount
        self.fees = fees
        if(timestamp == None):
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp

        if(is_coinbase == True):
            self.__set_coinbase_transaction()

    def set_id(self, id):
        self.id = id

    def get_transaction_data_as_dict(self):
        return({"sender_name": self.sender_name, 
                "receiver_name": self.receiver_name, 
                "amount": self.amount, 
                "is_coinbase": self.is_coinbase,
                "fees": self.fees,
                "id": self.id,
                "timestamp": self.timestamp})
    
    def load_all_from_dict(self, transaction_dict):
        self.sender_name = transaction_dict["sender_name"]
        self.receiver_name = transaction_dict["receiver_name"]
        self.amount = transaction_dict["amount"]
        self.is_coinbase = transaction_dict["is_coinbase"]
        self.timestamp = transaction_dict["timestamp"]
        self.fees = transaction_dict["fees"]
        self.id = transaction_dict["id"]
    
    def __set_coinbase_transaction(self):
        self.is_coinbase = True
        self.sender_name = "coinbase"
        self.receiver_name = None
        self.amount = self.fees + BLOCK_REWARD
        self.timestamp = time.time()

    def get_transaction_data_as_str(self):
        #dict to str
        return(str(self.get_transaction_data_as_dict()))

    

    