from ecdsa import SigningKey, SECP256k1
from hashlib import sha256, new
import base58
import json
import os
from datetime import datetime
from colorama import init, Fore, Back


class IdentityManager:

    wallet_pattern = ["created_at", "owner_name", "amount", "private_key", "public_address", "password"]

    def generate_keys(self):
        private_key = SigningKey.generate(curve=SECP256k1, hashfunc=sha256)
        public_key = private_key.verifying_key

        public_base_58 = base58.b58encode(public_key.to_string())

        return private_key.to_string().hex(), public_base_58

    def __save_wallet(self, owner_name, data):
        file_path = owner_name + ".cryptowallet"
        json_string = json.dumps(data, indent=4)

        if not os.path.exists(file_path):
                if '/' not in file_path and '\\' not in file_path:
                    file_path = "./" + file_path
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as json_file:
            json_file.write(json_string)

    @staticmethod
    def __hex_to_bytes(key):
        return bytes.fromhex(key)
    
    @staticmethod
    def __base58_to_bytes(key):
        return base58.b58decode(key)

    @staticmethod
    def __ripemd160(data):
        return new('ripemd160', data)

    def open_wallet(self, file_path, password):
        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
            
            idx = 0 
            for obj in data.keys():
                if(obj != self.wallet_pattern[idx]):
                    print(Back.RED + "Wrong wallet format!")
                    return None
                else:
                    idx += 1

            test_priv = SigningKey.from_string(self.__hex_to_bytes(data['private_key']), curve=SECP256k1, hashfunc=sha256)
            test_pub = self.__base58_to_bytes(data['public_address']) #VerifyingKey.from_string(self.__base58_to_bytes())

            if (test_priv.verifying_key.to_string() != test_pub):
                print(Back.RED + "Private key and public key are not related!")
                return None
            
            data_password = data['password']

            if(self.__hash_password(password) != data_password):
                print(Back.RED + "Wrong password!")
                return None
            
            return data
        except FileNotFoundError:
            print(Back.RED + f"File '{file_path}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(Back.RED + f"Error decoding CryptoWallet: {e}")
            return None

    def create_wallet(self, owner_name, password):
        wallet_dict = {}
        wallet_dict['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wallet_dict['owner_name'] = owner_name.split("/")[-1]
        wallet_dict['amount'] = 0
        priv_key, pub_key = self.generate_keys()
        wallet_dict['private_key'] = priv_key
        wallet_dict['public_address'] = pub_key.decode('utf-8')
        #Hashed password sha256
        wallet_dict['password'] = self.__hash_password(password)
        self.__save_wallet(owner_name, wallet_dict)
        return wallet_dict
    
    def add_amount_to_wallet(self, path, amount):
        wallet = self.open_wallet(path)
        if(wallet == None):
            return
        w_amount = float(wallet['amount'])
        w_amount += float(amount)
        wallet['amount'] = str(w_amount)
        self.__save_wallet(wallet['owner_name'], wallet)

    def get_wallet_amount(self, path):
        wallet = self.open_wallet(path)
        if(wallet == None):
            return
        return float(wallet['amount'])
    
    def __hash_password(self, password):
        return new('sha256', password.encode('utf-8')).hexdigest()

im = IdentityManager()
im.generate_keys()