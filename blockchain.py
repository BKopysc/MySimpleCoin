from blockchain_block import BlockchainBlock
from transaction_data import TransactionData

class Blockchain():
    def __init__(self):
        self.head = None
        self.difficulty = 5
        self.reward = 20
        self.pending_transactions = []
        self.chain = [self.__create_genesis_block()]

    def __create_genesis_block(self):
        # Genesis block
        self.head = BlockchainBlock(previous_hash=None, transactions=[], index=0)
        return(self.head)


    def add_block(self, transaction):
        current_block = self.get_last_block()
        if(current_block != None):  
            block = BlockchainBlock(previous_hash=current_block.get_hash(), transactions=transaction, index=current_block.index+1)
            self.chain.append(block)
    
    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def add_many_transactions(self, transactions):
        for transaction in transactions:
            self.pending_transactions.append(transaction)

    def get_blockchain_as_list(self):
        blockchain_list = []
        for block in self.chain:
            blockchain_list.append(block.get_block_as_dict())
        return(blockchain_list)
    
    def get_last_block(self):
        return self.chain[-1]
    
    def is_chain_valid(self):
        i = 1
        previous_block = self.chain[0]
        while(i < len(self.chain)):
            current_block = self.chain[i]
            if(current_block.previous_hash != previous_block.get_hash()):
                return(False)
            previous_block = current_block
            i+=1
        return(True)
    
    def mine_pending_transactions(self, miner_name, transaction_ids):

        # Get transactions to mine
        todo_transactions = []
        for transaction in self.pending_transactions:
            if(transaction.id in transaction_ids):
                todo_transactions.append(transaction)

        if(len(todo_transactions) == 0):
            return(self.__return_status("error", "No transactions to mine"))

        #Remove transactions from pending
        for transaction in todo_transactions:
            self.pending_transactions.remove(transaction)

        if(len(todo_transactions) == 0):
            return(self.__return_status("error", "No transactions to mine"))
        
        # Create new block and mine it
        newBlock = BlockchainBlock(previous_hash=self.get_last_block().get_hash(), transactions=todo_transactions, index=self.get_last_block().index+1)
        newBlock.mine_block(self.difficulty)

        
        # Add reward transaction to pending transactions
        rewardTransaction = TransactionData(sender_name="network", receiver_name=miner_name, amount=self.reward)
        self.pending_transactions.append(rewardTransaction)

        print("Block mined!" + " miner: " + miner_name)

        for block in self.chain:
            if(block.get_hash() == newBlock.get_hash()):
                return(self.__return_status("error", "Block already exists"))
        self.chain.append(newBlock)
        
        return(self.__return_status("success", "Block mined!"))

    def get_pending_transactions_str(self):
        return(list(map(lambda x: x.get_transaction_data_as_str(), self.pending_transactions)))
    
    def __return_status(self, status, message):
        return({'status': status, 'message': message})
        

        
