import time

class TransactionData:
    def __init__(self, sender_name: str, receiver_name:str , amount: float, timestamp: float = None):
        self.sender_name = sender_name
        self.receiver_name = receiver_name
        self.amount = amount
        if(timestamp == None):
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp

    def get_transaction_data_as_dict(self):
        return({"sender_name": self.sender_name, "receiver_name": self.receiver_name, "amount": self.amount, "timestamp": self.timestamp})


    def get_transaction_data_as_str(self):
        #dict to str
        return(str(self.get_transaction_data_as_dict()))

    

    