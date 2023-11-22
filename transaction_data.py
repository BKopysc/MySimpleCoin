import time
import uuid

class TransactionData:
    def __init__(self, sender_name: str = "", receiver_name:str = "" , amount: float = 0, timestamp: float = None):
        self.id: int = uuid.uuid4().int
        self.sender_name = sender_name
        self.receiver_name = receiver_name
        self.amount = amount
        if(timestamp == None):
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp

    def set_id(self, id):
        self.id = id

    def get_transaction_data_as_dict(self):
        return({"sender_name": self.sender_name, 
                "receiver_name": self.receiver_name, 
                "amount": self.amount, 
                "id": self.id,
                "timestamp": self.timestamp})
    
    def load_all_from_dict(self, transaction_dict):
        self.sender_name = transaction_dict["sender_name"]
        self.receiver_name = transaction_dict["receiver_name"]
        self.amount = transaction_dict["amount"]
        self.timestamp = transaction_dict["timestamp"]
        self.id = transaction_dict["id"]

    def get_transaction_data_as_str(self):
        #dict to str
        return(str(self.get_transaction_data_as_dict()))

    

    