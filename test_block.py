from blockchain_block import BlockchainBlock
from blockchain import Blockchain
from transaction_data import TransactionData

# block1 = BlockchainBlock()
# block1_hash = block1.get_hash()
# block2 = BlockchainBlock(previous_hash=block1_hash)
# print(block1_hash)
# print(block2.get_block_as_dict())

blockchain = Blockchain()
t1 = TransactionData("user1", "user2", 10)
t2 =  TransactionData("user2", "user1", 5)
blockchain.add_transaction(t1)
blockchain.add_transaction(t2)
blockchain.get_pending_transactions()
print(blockchain.get_pending_transactions())
# blockchain.add_many_transactions([t1,t2])
# blockchain.mine_pending_transactions("miner1", [t1.id])
# print(blockchain.get_pending_transactions_str())
# blockchain.mine_pending_transactions("miner2", [t2.id])
# print(blockchain.get_pending_transactions_str())
#res = blockchain.get_blockchain_as_list()
#check = blockchain.is_chain_valid()
#print(res)
#print('is chain valid: ', check)

