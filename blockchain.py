from blockchain_block import BlockchainBlock
from transaction_data import TransactionData
from hashlib import sha256
import os
from dotenv import load_dotenv

load_dotenv()
BLOCK_REWARD = float(os.getenv("BLOCK_REWARD"))

class Blockchain():
    def __init__(self):
        self.head = None
        self.difficulty = 5
        self.reward = BLOCK_REWARD
        self.pending_transactions: list[TransactionData] = []
        self.previously_mined_transactions = []
        self.chain = [self.__create_genesis_block()]

    def __create_genesis_block(self):
        # Genesis block
        genesis_block = BlockchainBlock(previous_hash=None, transactions=[])
        self.head = genesis_block
        return(self.head)


    def add_block(self, transactions: list[TransactionData]):
        current_block = self.get_last_block()
        if(current_block != None):
            new_transactions = []

            base_fees = 0
            for transaction in transactions:
                base_fees += transaction.fees
                new_transactions.append(transaction)
            
            coinbase_trans = TransactionData(is_coinbase=True, fees=base_fees)
            # insert at start of list
            new_transactions.insert(coinbase_trans, 0)

            block = BlockchainBlock(previous_hash=current_block.get_hash(), transactions=new_transactions)
            self.chain.append(block)
    
    def add_received_block(self, block):
        self.chain.append(block)

    def add_transaction(self, transaction: TransactionData):
        if(transaction.id in self.pending_transactions):
            return(self.__return_status("error", "Transaction already exists"))
        self.pending_transactions.append(transaction)

    def pop_transaction(self, transactionId):
        for transaction in self.pending_transactions:
            if(transaction.id == transactionId):
                self.pending_transactions.remove(transaction)
                return(self.__return_status("success", "Transaction removed"))
        return(self.__return_status("error", "Transaction not found"))

    def add_many_transactions(self, transactions):
        for transaction in transactions:
            self.pending_transactions.append(transaction)

    def get_blockchain_as_dict(self):
        blockchain_dict = {
            "head": self.head.get_block_as_dict(),
            "difficulty": self.difficulty,
            "reward": self.reward,
            "pending_transactions": [],
            "chain": [],
        }
        
        for block in self.chain:
            blockchain_dict["chain"].append(block.get_block_as_dict())
        
        for transaction in self.pending_transactions:
            blockchain_dict["pending_transactions"].append(transaction.get_transaction_data_as_dict())

        return(blockchain_dict)
    
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
            self.previously_mined_transactions.append(transaction)

        if(len(todo_transactions) == 0):
            return(self.__return_status("error", "No transactions to mine"))
        
        # Create new block and mine it
        newBlock = BlockchainBlock(previous_hash=self.get_last_block().get_hash(), transactions=todo_transactions)
        newBlock.mine_block(self.difficulty)

        
        # Add reward transaction to pending transactions
        rewardTransaction = TransactionData(sender_name="network", receiver_name=miner_name, amount=self.reward)
        self.pending_transactions.append(rewardTransaction)

        #print("Block mined!" + " miner: " + miner_name)

        for block in self.chain:
            if(block.get_hash() == newBlock.get_hash()):
                return(self.__return_status("error", "Block already exists"))
        self.chain.append(newBlock)

        return(self.__return_status("success", "Block mined!", newBlock, rewardTransaction))

    def get_pending_transactions(self):
        temp_list = []
        for transaction in self.pending_transactions:
            temp_list.append(transaction.get_transaction_data_as_dict())

        return(temp_list)
        
    
    def __return_status(self, status, message, block: BlockchainBlock=None, new_transactions: TransactionData=None):
        return({'status': status, 'message': message, 'block': block, 'new_transactions': new_transactions})
        
    def check_if_not_mined(self, transaction_id):
        for transaction in self.previously_mined_transactions:
            if(transaction.id == transaction_id):
                return(True)
        return(False)
    
    def validate_new_block(self, block: BlockchainBlock):
        if(block.previous_hash != self.get_last_block().get_hash()):
            print("Error: Previous hash not valid")
            print(block.previous_hash)
            print(self.get_last_block.get_hash())
            return(False)
        if(block.get_hash() != block.generate_hash()):
            print("Error: Hash not valid")
            return(False)
        
        self.add_received_block(block)
        return(True)
    
    def load_all_from_dict(self, blockchain_dict):
        headBlock = BlockchainBlock()
        headBlock.load_all_from_dict(blockchain_dict["head"])
        self.head = headBlock
        self.difficulty = blockchain_dict["difficulty"]
        self.reward = blockchain_dict["reward"]

        self.pending_transactions = []
        for transaction_dict in blockchain_dict["pending_transactions"]:
            transaction = TransactionData()
            transaction.load_all_from_dict(transaction_dict)
            self.pending_transactions.append(transaction)
        
        self.previously_mined_transactions = []

        self.chain = []
        for block_dict in blockchain_dict["chain"]:
            block = BlockchainBlock()
            block.load_all_from_dict(block_dict)
            self.chain.append(block)

    # def get_blockchain_as_dict(self):
    #     return({"head": self.head, 
    #             "difficulty": self.difficulty, 
    #             "reward": self.reward, 
    #             "pending_transactions": self.pending_transactions, 
    #             "chain": self.chain})
    
    def verify_hash_obj(self):
        b_hash = sha256(str(self.get_blockchain_as_dict()).encode('utf-8')).hexdigest()
        return(b_hash)
