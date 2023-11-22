from blockchain_block import BlockchainBlock
from blockchain import Blockchain
from transaction_data import TransactionData

blockchain = Blockchain()
t1 = TransactionData("user1", "user2", 10)
t2 =  TransactionData("user2", "user1", 5)
blockchain.add_transaction(t1)
blockchain.add_transaction(t2)
blockchain.get_pending_transactions()
hsh = blockchain.verify_hash_obj()
print(blockchain.get_pending_transactions())
print(blockchain.get_last_block().get_block_as_dict())
res = blockchain.mine_pending_transactions("miner1", [t1.id])
print(res)
print(res["block"].get_block_as_dict())
print(blockchain.get_last_block().generate_hash())


