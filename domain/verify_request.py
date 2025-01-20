import base64

import orjson
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class VerifyRequest:

    def __order_dict(self, dictionary):
        result = {}
        for k, v in sorted(dictionary.items()):
            if isinstance(v, dict):
                result[k] = self.__order_dict(v)
            else:
                result[k] = v
        return result

    def verify_signature(self, data: dict, signature: str, public_key: str) -> bool:
        sorted_message = orjson.dumps(self.__order_dict(data))
        digest = SHA256.new(sorted_message)

        public_key = RSA.importKey(public_key)
        sig = base64.b64decode(signature)

        verifier = PKCS1_v1_5.new(public_key)
        return verifier.verify(digest, sig)
