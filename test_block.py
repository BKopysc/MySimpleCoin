from blockchain_block import BlockchainBlock

block1 = BlockchainBlock()
block1_hash = block1.get_hash()
block2 = BlockchainBlock(previous_hash=block1_hash)
print(block1_hash)
print(block2.get_block_as_dict())