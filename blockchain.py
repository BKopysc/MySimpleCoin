from blockchain_block import BlockchainBlock

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
    
    def mine_pending_transactions(self, miner_name):
        newBlock = BlockchainBlock(previous_hash=self.get_last_block().get_hash(), transactions=self.pending_transactions, index=self.get_last_block().index+1)
        newBlock.mine_block(self.difficulty)

        print("Block mined!")
        self.chain.append(newBlock)

        
