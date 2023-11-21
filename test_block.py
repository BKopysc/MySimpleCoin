from blockchain_block import BlockchainBlock
from blockchain import Blockchain

# block1 = BlockchainBlock()
# block1_hash = block1.get_hash()
# block2 = BlockchainBlock(previous_hash=block1_hash)
# print(block1_hash)
# print(block2.get_block_as_dict())

blockchain = Blockchain()
blockchain.add_transaction("transaction1")
blockchain.mine_pending_transactions("miner1")
#res = blockchain.get_blockchain_as_list()
#check = blockchain.is_chain_valid()
#print(res)
#print('is chain valid: ', check)

