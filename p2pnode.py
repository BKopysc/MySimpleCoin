from p2pnetwork.node import Node
import time
from colorama import Fore, Style
from ecdsa import SigningKey, VerifyingKey , SECP256k1
from hashlib import sha256, new
import base58

class P2PNode (Node):
    # Python class constructor
    def __init__(self, host, port, seed_node_info=None, id=None, private_key=None, callback=None, max_connections=0):
        super(P2PNode, self).__init__(host, port, id, callback, max_connections)
        self.seed_node_info = seed_node_info
        self.private_key = private_key
        self.available_nodes = dict()
        self.nodes_connected = dict()
        self.correct_auth_signature = "auth_ok"
        self.start()
        time.sleep(1)

        if(seed_node_info is not None):
            self.connect_with_node(seed_node_info["ip"], seed_node_info["port"])
            time.sleep(1)
        
    def outbound_node_connected(self, connected_node):
        #print("outbound_node_connected: " + connected_node.id)
        #self.__send_verify_signature()
        self.__send_verify_signature()
        
        
    def inbound_node_connected(self, connected_node):
        #print("inbound_node_connected: " + connected_node.id)
        #self.__send_verify_signature()
        pass

    def inbound_node_disconnected(self, connected_node):
        #print("inbound_node_disconnected: " + connected_node.id)
        pass

    def outbound_node_disconnected(self, connected_node):
        #print("outbound_node_disconnected: " + connected_node.id)
        pass

    def node_message(self, connected_node, data):
        #print(Fore.GREEN + "Data received: " + str(data))
        if("_type" in data):
            if(data["_type"] == "new_node"):
                self.available_nodes = data["node_registry"]
                print(Fore.CYAN + ">> New list: " + str(self.available_nodes))
                self.__connect_to_new_nodes()
            elif(data['_type'] == "verify_node"):
                res = self.__verify_signature(data["signed_signature"], connected_node.id)
                if(res):
                    print(Fore.GREEN + ">>>> Node verified! [" + connected_node.id + "]")
                else:
                    print(Fore.RED + ">>>> Node not verified! [" + connected_node.id + "]")

                #print(Fore.YELLOW + "signature: " + data["signed_signature"])

        
    @staticmethod
    def __hex_to_bytes(key):
        return bytes.fromhex(key)
    
    @staticmethod
    def __base58_to_bytes(key):
        return base58.b58decode(key)
    
    def __sign_with_private_key(self, data):
        priv_k = SigningKey.from_string(self.__hex_to_bytes(self.private_key), curve=SECP256k1, hashfunc=sha256)
        signed = priv_k.sign_deterministic(data.encode("utf-8"), hashfunc=sha256)
        return signed.hex()


    def __verify_signature(self, signature, public_address):
        #weryfikacja podpisu
        decrypted_public_key = self.__base58_to_bytes(public_address)
        public_key = VerifyingKey.from_string(decrypted_public_key, curve=SECP256k1, hashfunc=sha256)
        print("\nSignature: " + signature + "\n")
        try:
            public_key.verify(self.__hex_to_bytes(signature), self.correct_auth_signature.encode('utf-8'), sha256)
            return True
        except:
            return False

    def __send_verify_signature(self):
        signed_signature = self.__sign_with_private_key(self.correct_auth_signature)
        self.send_to_nodes({"_type": "verify_node", "signed_signature": signed_signature})


    def __connect_to_new_nodes(self):
        for node_id, node_data in self.available_nodes.items():
            if(node_id not in self.nodes_connected):
                if(node_data["ip"] == str(self.host) and node_data["port"] == str(self.port) and node_id == str(self.id)):
                    continue
                self.connect_with_node(str(node_data["ip"]), int(node_data["port"]))
                time.sleep(1)
                self.nodes_connected[node_id] = node_data
                print(Fore.YELLOW + ">> Connected to: " + str(node_data))
                return

    def send_ping(self):
        self.send_to_nodes("ping")
    
    def send_pong(self):
        self.send_to_nodes("pong")

    def received_ping(self):
        self.send_pong()
        
    def node_disconnect_with_outbound_node(self, connected_node):
        #print("node wants to disconnect with oher outbound node: " + connected_node.id)
        pass
        
    def node_request_to_stop(self):
        self.send_to_nodes({"_type": "disconnect"})
        print(Fore.RED + "node is requested to stop!")


