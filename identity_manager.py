from ecdsa import SigningKey, SECP256k1
from hashlib import sha256, new
import base58
import json
import os
from datetime import datetime
from colorama import init, Fore, Back
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64


class IdentityManager:

    salt = bytes("SimpleCoin", encoding='utf-8')

    wallet_pattern = ["created_at", "owner_name", "amount", "private_key", "public_address", "password"]

    def generate_keys(self):
        private_key = SigningKey.generate(curve=SECP256k1, hashfunc=sha256)
        public_key = private_key.verifying_key

        public_base_58 = base58.b58encode(public_key.to_string())

        return private_key.to_string().hex(), public_base_58

    def __save_wallet(self, owner_name, data, password = ""):
        file_path = owner_name + ".cwallet"
        json_string = json.dumps(data, indent=4)

        if not os.path.exists(file_path):
                if '/' not in file_path and '\\' not in file_path:
                    file_path = "./" + file_path
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

        #encrypted_data = self.__encrypt_AES(json_string, password, self.salt)

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

    def open_wallet(self, file_path, password, is_pass_hashed = False):
        try:
            encrypted_data = ""
            with open(file_path, "r") as json_file:
                #data = json.load(json_file)
                encrypted_data = json_file.read()
            
            #hash_password = self.__hash_password(password)

            #decrypted_data = self.__decrypt_AES(encrypted_data, hash_password, self.salt)
            #print(decrypted_data)

            data = json.loads(encrypted_data)
            
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

            input_password = password

            if(not is_pass_hashed):
                input_password = self.__hash_password(password)

            if(input_password != data_password):
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
        self.__save_wallet(owner_name, wallet_dict, password)
        return wallet_dict
    
    def add_amount_to_wallet(self, path, amount):
        wallet = self.open_wallet(path)
        if(wallet == None):
            return
        w_amount = float(wallet['amount'])
        w_amount += float(amount)
        wallet['amount'] = str(w_amount)
        self.__save_wallet(wallet['owner_name'], wallet)

    def get_wallet_amount(self, path, hash_password):
        wallet = self.open_wallet(path, hash_password, is_pass_hashed=True)
        if(wallet == None):
            return
        return float(wallet['amount'])
    
    def __hash_password(self, password):
        return new('sha256', password.encode('utf-8')).hexdigest()
    
    # def __encrypt_file_with_pass(self, hash_password, data):
    #     print(data)
    #     paded_key = self.__pad_key(hash_password, data)
    #     encrypted_data = self.__str_xor(data, paded_key)
    #     return encrypted_data

    # def __decrypt_file_with_pass(self, hash_password, data):
    #     paded_key = self.__pad_key(hash_password, data)
    #     decrypted_data = self.__str_xor(data, paded_key)
    #     return decrypted_data

    # def __pad_key(self, key, data):
    #     padded_key="" # padded key for text len 
    #     key_ctr=0
    #     for char in data:
    #         padded_key+=key[key_ctr]
    #         key_ctr += 1
    #         if(key_ctr >= len(key)):
    #             key_ctr = 0      
    #     return padded_key  
    
    # def __str_xor(self, s1, s2):
    #     return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])
    
    # def __encrypt_AES(self, plain_text, password, salt):
    #     key = self.__derive_key(password, salt)
    #     cipher = Cipher(algorithms.AES(key), modes.CFB(), backend=default_backend())
    #     encryptor = cipher.encryptor()
    #     padder = padding.PKCS7(128).padder()
    #     padded_data = padder.update(plain_text.encode()) + padder.finalize()
    #     encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    #     return encrypted_data

    # def __decrypt_AES(self, encrypted_data, password, salt):
    #     key = self.__derive_key(password, salt)
    #     cipher = Cipher(algorithms.AES(key), modes.CBC(), backend=default_backend())
    #     decryptor = cipher.decryptor()
    #     decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    #     unpadder = padding.PKCS7(128).unpadder()
    #     decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    #     return decrypted_data.decode()
        
    # def __derive_key(self, password, salt):
    #     kdf = PBKDF2HMAC(
    #         algorithm=hashes.SHA256(),
    #         iterations=10, 
    #         salt=salt,
    #         length=32
    #     )
    #     return base64.urlsafe_b64encode(kdf.derive(password.encode()))


im = IdentityManager()
im.generate_keys()