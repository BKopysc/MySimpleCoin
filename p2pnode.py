from p2pnetwork.node import Node
import time
from colorama import Fore, Style
from ecdsa import SigningKey, VerifyingKey , SECP256k1
from hashlib import sha256, new
import base58
from blockchain import Blockchain
from transaction_data import TransactionData
from blockchain_block import BlockchainBlock
from identity_manager import IdentityManager

class P2PNode (Node):
    # Python class constructor
    def __init__(self, host, port, seed_node_info=None, id=None, private_key=None, callback=None, wallet_path="",max_connections=0):
        super(P2PNode, self).__init__(host, port, id, callback, max_connections)
        self.seed_node_info = seed_node_info
        self.private_key = private_key
        self.available_nodes = dict()
        self.nodes_connected = dict()
        self.blockchain = Blockchain()
        self.wallet_path = wallet_path
        self.identityManager = IdentityManager()
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
        self.__send_blockchain()
        
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
        #print("Data received: " + str(data) + " from " + connected_node.id)
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

            elif(data['_type'] == "ping"):
                self.send_pong()

            elif(data['_type'] == "pong"):
                print(Fore.YELLOW + ">>>> PONG received!")

            elif(data['_type'] == "new_transaction"):
                print(Fore.YELLOW + ">>>> New transaction received!")
                res=self.load_transaction_from_network(data["transaction"])
                self.send_trans_verify(data["transaction"]["id"], res)

            elif(data['_type'] == "new_block"):
                print(Fore.YELLOW + ">>>> New block received!")
                self.validate_and_load_new_block(data["block"])

            elif(data['_type'] == "pop_transaction"):
                print(Fore.YELLOW + ">>>> Pop transaction received!")
                pop_list = data["transaction_id"]
                for transaction_id in pop_list:
                    self.pop_transaction_from_network(transaction_id)

            elif(data['_type'] == "disconnect"):
                #self.available_nodes.pop(connected_node.id)
                pass

            elif(data['_type'] == "new_blockchain"):
                print(Fore.YELLOW + ">>>> New blockchain received!")
                self.load_blockchain_from_dict(data["blockchain"])

            elif(data['_type'] == "mining_result_confirmed"):
                print(Fore.YELLOW + ">>>> Mining result confirmed!")
                block_hash = data["block_hash"]
                self.recieve_mining_confirmed(block_hash)
                #self.mine_transaction(data["transaction_id"])

            else:
                print(Fore.RED + ">>>> Received Unknown data type: " + str(data))
            
                #print(Fore.YELLOW + "signature: " + data["signed_signature"])

    # ------- AUTHENTICATION METHODS ------- #

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
        self.send_to_nodes({"_type": "verify_node", "signed_signature": signed_signature}, exclude=[self.id])


    def connect_to_new_node(self, ip, port):
        self.connect_with_node(ip, port)
        time.sleep(1)

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
        self.send_to_nodes({"_type": "ping"}, exclude=[self.id])
    
    def send_pong(self):
        self.send_to_nodes({"_type": "pong"}, exclude=[self.id])

    def received_ping(self):
        self.send_pong()
        
    def node_disconnect_with_outbound_node(self, connected_node):
        #print("node wants to disconnect with oher outbound node: " + connected_node.id)
        pass
        
    def node_request_to_stop(self):
        self.send_to_nodes({"_type": "disconnect"})
        print(Fore.RED + "node is requested to stop!")

    def send_trans_verify(self, transaction_id, verdict: bool):
        self.send_to_nodes({"_type": "transaction_verify", "transaction_id": transaction_id, "verdict": verdict})

# ------- BLOCKCHAIN METHODS ------- #

    def get_transactions(self):
        return self.blockchain.get_pending_transactions()
    
    def send_money(self, receiver, amount):
        owned_amount = self.identityManager.get_wallet_amount(self.wallet_path)
        if(owned_amount < amount):
            print(Fore.RED + "Error: Not enough money!")
            return
        self.add_transaction(self.id, receiver, amount)
        #self.identityManager.add_amount_to_wallet(self.wallet_path, -amount)
    
    def add_transaction(self, sender, receiver, amount):
        transaction = TransactionData(sender_name=sender, receiver_name=receiver, amount=amount, sender_private_key=self.private_key)
        self.blockchain.add_transaction(transaction)
        self.send_to_nodes({"_type": "new_transaction", "transaction": transaction.get_transaction_data_as_dict()}, exclude=[self.id])

    # Recieve transaction verification and count money
    def recieve_transaction_verification(self, transaction_id, verdict):
        if(verdict == True):
            transaction = self.blockchain.get_pending_transaction_by_id(transaction_id)
            if(transaction == None):
                print(Fore.RED + "Error: Transaction not found! <transaction verification>")
                return
            
            if(transaction.verified == True):
                return
            
            if(self.blockchain.check_if_not_mined([transaction_id]) == False):
                print(Fore.RED + "Error: Transaction already mined! <transaction verification>")
                return

            print(Fore.GREEN + "Transaction verified! <transaction verification>")
            
            self.identityManager.add_amount_to_wallet(self.wallet_path, -transaction.amount)
            self.blockchain.set_pending_transaction_verify(transaction_id, True)
        else:
            print(Fore.RED + "Error: Transaction not verified! <transaction verification>")
            self.blockchain.pop_transaction(transaction_id)

    def mine_transaction(self, transaction_ids: list[int]):
        miner_name = self.id
        # Mine block
        mine_result = self.blockchain.mine_pending_transactions(miner_name, transaction_ids)

        if(mine_result["status"] == "success"):
            if(self.blockchain.check_if_not_mined(transaction_ids) == False):
                print(Fore.RED + "Error: Transaction already mined!")
                return
            else:
                mined_block: BlockchainBlock = mine_result["block"]
                rewardTransaction: TransactionData = mine_result["new_transactions"]
                self.send_to_nodes({"_type": "new_block", "block": mined_block.get_block_as_dict()}, exclude=[self.id])
                self.send_to_nodes({"_type": "new_transaction", "transaction": rewardTransaction.get_transaction_data_as_dict()}, exclude=[self.id])
                self.send_to_nodes({"_type": "pop_transaction", "transaction_id": transaction_ids})
                print(Fore.GREEN + "Block mined! " + str(mined_block.get_block_as_dict()))

                #transfer_trans: list[TransactionData] = self.blockchain.check_if_previous_trans_is_for_you(mined_block, miner_name)
                #self.add_amount_from_transaction(transfer_trans)
                
        else:
            print(Fore.RED + "Error: " + mine_result["message"])

    def recieve_mining_confirmed(self, block_hash: str):
        # Count confirmations
        # If confirmations > 50% of nodes -> confirm
        # If confirm -> add to blockchain

        res_block = self.blockchain.get_block_by_hash(block_hash)
        if(res_block == None):
            print(Fore.RED + "Error: Confirmed block not found!")
            return

        transfer_trans: list[TransactionData] = self.blockchain.check_if_previous_trans_is_for_you(res_block, self.id)
        self.add_amount_from_transaction(transfer_trans)

        
    def add_amount_from_transaction(self, transaction_list: list[TransactionData]):
        final_amount = 0

        for transaction in transaction_list:
            if(transaction.receiver_name == self.id):
                final_amount += transaction.amount
        
        if(final_amount > 0):
            self.identityManager.add_amount_to_wallet(self.wallet_path, final_amount)
            print(Fore.MAGENTA + "Amount added to wallet: " + str(final_amount))

    def load_transaction_from_network(self, transaction_dict):
        transaction = TransactionData()
        transaction.load_all_from_dict(transaction_dict)

        if(transaction.id in self.blockchain.get_pending_transactions()):
            return True

        if(transaction.verify_signature(sender_public_key=transaction.sender_name) == False):
            print(transaction.get_transaction_data_as_str())
            print(Fore.RED + "Error: Transaction signature is not valid! <load transaction>")
            return False

        if(self.blockchain.check_if_target_has_amount_in_blockchain(transaction.sender_name, transaction.amount) == False):
            print(Fore.RED + "Error: Sender has not enough money! <load transaction>")
            return False
        
        self.blockchain.add_transaction(transaction)
        return True

    def load_blockchain_from_dict(self, blockchain_dict):
        tempBlockChain = Blockchain()
        tempBlockChain.load_all_from_dict(blockchain_dict)
        if(tempBlockChain.verify_hash_obj() != self.blockchain.verify_hash_obj()):
            self.blockchain = tempBlockChain
            print(Fore.GREEN + ">>>> Blockchain updated!")
        self.blockchain.load_all_from_dict(blockchain_dict)

    def validate_and_load_new_block(self, block):
        tempBlock = BlockchainBlock()
        tempBlock.load_all_from_dict(block)
        res = self.blockchain.validate_new_block(tempBlock, public_address=self.id)
        if(res['status'] == "error"):
            print(Fore.RED + "Error: Block not valid!")
        elif (res['status'] == "added"):
            self.send_to_nodes({"_type": "mining_result_confirmed", "block_hash": tempBlock.get_hash()})

            # TODO: CHANGE THIS TO BE CONFIRMED BY OTHER NODES
            if type(res) is list:
                self.add_amount_from_transaction(res)
        elif (res['status'] == "fork"):
            print(Fore.YELLOW + "Fork detected!")
            self.send_to_nodes({"_type": "mining_result_confirmed", "block_hash": tempBlock.get_hash()})
        
    def pop_transaction_from_network(self, transaction_id):
        self.blockchain.pop_transaction(transaction_id)

    def __send_blockchain(self):
        self.send_to_nodes({"_type": "new_blockchain", "blockchain": self.blockchain.get_blockchain_as_dict()})

    
    def set_wallet_path(self,path):
        self.wallet_path = path
    
    





