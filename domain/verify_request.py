import base64

import orjson
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from fastapi.logger import logger


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
        try:
            sig = base64.b64decode(signature)
        except Exception as e:
            logger.error(f"Помилка при декодуванні підпису: {e}")
            return False

        verifier = PKCS1_v1_5.new(public_key)
        is_verified = verifier.verify(digest, sig)

        logger.info(f"Результат перевірки підпису: {'вірний' if is_verified else 'не вірний'}")

        return is_verified

