from p2pnetwork.node import Node
from colorama import Fore, Style


class SeedNode(Node):
    # Python class constructor
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(SeedNode, self).__init__(host, port, id, callback, max_connections)
        self.node_registry = dict()

    def outbound_node_connected(self, connected_node):
        #print("outbound_node_connected: " + connected_node.id)
        pass
        
    def inbound_node_connected(self, connected_node):
        #print("inbound_node_connected: " + connected_node.id)
        node_data = {"ip": connected_node.host, "port": connected_node.port}
        self.node_registry[connected_node.id] = node_data
        print(Fore.GREEN + "+ New node registered: " + str(node_data) + " from " + connected_node.id)
        print(Fore.WHITE + ">> New list: " + str(self.node_registry))
        self.send_to_nodes({"_type": "new_node", "node_registry": self.node_registry})

    def inbound_node_disconnected(self, connected_node):
        pass

    def outbound_node_disconnected(self, connected_node):
        pass
        # self.node_registry.pop(connected_node.id)
        # print("inbound_node_disconnected: " + connected_node.id)
        # print("New list: " + str(self.node_registry))

    def node_message(self, connected_node, data):
        if("_type" in data):
            if(data["_type"] == "disconnect"):
                self.node_registry.pop(connected_node.id)
                print(Fore.RED + "- Node " + connected_node.id + " disconnected")
                print(Fore.WHITE + ">> New list: " + str(self.node_registry))
        
    def node_disconnect_with_outbound_node(self, connected_node):
        #print("node wants to disconnect with oher outbound node: " + connected_node.id)
        pass
        
    def node_request_to_stop(self):
        #print("node is requested to stop!")
        pass