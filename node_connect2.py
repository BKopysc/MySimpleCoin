import sys
import time
from p2pnode import P2PNode

node = P2PNode("127.0.0.1", 9001, seed_node_info = {"ip": "127.0.0.1", "port": 6000}, private_key = "a40f81aa02001347124cd450c33c39268589b7c289606222a2a8084e072b2e35")
time.sleep(10)

# Do not forget to start your node!
#node.start()

node.stop()