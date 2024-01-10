from ecdsa import SigningKey, SECP256k1, VerifyingKey
from hashlib import sha256, new
import base58
import json

class KeyUtil:

    def __init__(self):
        pass

    def sign(self, private_key: str, data):
        try:
            sign_res = SigningKey.from_string(bytes.fromhex(private_key),hashfunc=sha256).sign(data.encode('utf-8'))
            return base58.b58encode(sign_res).decode('utf-8')
        except:
            return None
    
    def verify(self, public_key_b58: str, signature: str, data: str):
        try:
            public_decoded = base58.b58decode(public_key_b58)
            signature_decoded = base58.b58decode(signature)
            verify_res = VerifyingKey.from_string(public_decoded, hashfunc=sha256).verify(signature_decoded, data.encode('utf-8'))
            return verify_res
        except:
            return False
    
    def generate_keys(self):
        private_key = SigningKey.generate(hashfunc=sha256)
        public_key = private_key.verifying_key
        public_base_58 = base58.b58encode(public_key.to_string())
        return private_key.to_string().hex(), public_base_58.decode('utf-8')
    

# ku = KeyUtil()
# pr, pu = ku.generate_keys()
# print(pr)
# print(pu)
# data = json.dumps({"test": "test"})
# print(data)
# signature = ku.sign(pr, data)
# print(signature)
# print(ku.verify(pu, signature, data))