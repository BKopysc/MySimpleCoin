from ecdsa import SigningKey, SECP256k1
from hashlib import sha256, new
import base58
import json
import os
from datetime import datetime


class IdentityManager:

    wallet_pattern = ["created_at", "owner_name", "private_key", "public_address"]

    def generate_keys(self):
        private_key = SigningKey.generate(curve=SECP256k1, hashfunc=sha256)
        public_key = private_key.verifying_key

        public_double_hashed = self.__ripemd160(public_key.to_string()).digest()
        public_base_58 = base58.b58encode(public_double_hashed)

        return private_key.to_string().hex(), public_base_58

    def __save_wallet(self, owner_name, data):
        file_path = owner_name + ".cryptowallet"
        json_string = json.dumps(data, indent=4)

        if not os.path.exists(file_path):
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

    def open_wallet(self, file_path):
        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
            
            idx = 0 
            for obj in data.keys():
                if(obj != self.wallet_pattern[idx]):
                    print("Wrong wallet format!")
                    return None
                else:
                    idx += 1

            test_priv = SigningKey.from_string(self.__hex_to_bytes(data['private_key']), curve=SECP256k1, hashfunc=sha256)
            test_pub = self.__base58_to_bytes(data['public_address']) #VerifyingKey.from_string(self.__base58_to_bytes())

            if (self.__ripemd160(test_priv.verifying_key.to_string()).digest() != test_pub):
                print("Private key and public key are not related!")
                return None
            
            return data
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding CryptoWallet: {e}")
            return None

    def create_wallet(self, owner_name):
        wallet_dict = {}
        wallet_dict['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wallet_dict['owner_name'] = owner_name.split("/")[-1]
        priv_key, pub_key = self.generate_keys()
        wallet_dict['private_key'] = priv_key
        wallet_dict['public_address'] = pub_key.decode('utf-8')
        self.__save_wallet(owner_name, wallet_dict)
        return wallet_dict

