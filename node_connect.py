import sys
import time
from p2pnode import P2PNode

node = P2PNode("127.0.0.1", 10001, seed_node_info = {"ip": "127.0.0.1", "port": 6000}, private_key = "1612c59aade493160c4ee360124ff1f38ff178922720666b397092ecf864f0ff")
time.sleep(10)

# Do not forget to start your node!
#node.start()

node.stop()