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
        # Сортуємо дані перед серіалізацією
        sorted_message = orjson.dumps(self.__order_dict(data))
        logger.info(f"Сортування та серіалізація даних для підпису: {sorted_message.decode()}")

        # Створення хешу повідомлення
        digest = SHA256.new(sorted_message)

        # Логування хешу
        logger.info(f"Хеш (SHA256) для перевірки підпису: {digest.hexdigest()}")

        # Завантажуємо публічний ключ
        public_key = RSA.importKey(public_key)

        # Логування публічного ключа
        logger.info(f"Публічний ключ для перевірки підпису: {public_key.export_key().decode()}")

        # Декодуємо підпис з base64
        try:
            sig = base64.b64decode(signature)
            logger.info(f"Декодований підпис (base64): {sig.hex()}")
        except Exception as e:
            logger.error(f"Помилка при декодуванні підпису: {e}")
            return False

        # Перевірка підпису
        verifier = PKCS1_v1_5.new(public_key)
        is_verified = verifier.verify(digest, sig)

        # Логування результату перевірки
        logger.info(f"Результат перевірки підпису: {'вірний' if is_verified else 'не вірний'}")

        return is_verified

