import base64
import orjson
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from domain.verify_request import VerifyRequest
from fastapi.logger import logger


def order_dict(dictionary):
    result = {}
    for k, v in sorted(dictionary.items()):
        if isinstance(v, dict):
            result[k] = order_dict(v)
        else:
            result[k] = v
    return result


# Генерація підпису
def generate_signature(data: dict, private_key: str) -> str:
    """
    Генерує підпис для даних, використовуючи приватний ключ.
    """
    # Сортуємо дані перед серіалізацією
    sorted_message = orjson.dumps(order_dict(data))
    digest = SHA256.new(sorted_message)

    # Завантажуємо приватний ключ
    private_key = RSA.importKey(private_key)
    signer = PKCS1_v1_5.new(private_key)

    # Створюємо підпис
    signature = signer.sign(digest)

    # Повертаємо підпис у форматі base64
    return base64.b64encode(signature).decode()


# Тестові дані
data = {
    "account": {
        "account_id": "ab860855-137b-4ace-b8cb-834dfa99fffc",
        "balance": "140.52",
        "currency": "USD",
        "customer_id": "6406938403",
        "email": "denversmilla@gmail.com",
        "limit": "0.00",
        "spend": "0.00",
        "status": "CLOSED"
    },
    "action": "CLOSE_ACCOUNT",
    "exception": "",
    "success": True,
    "uid": "fcfcba60-b722-4171-8d7b-6e8d021861d8"
}

# Генерація пари ключів RSA
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Генерація підпису для даних
signature = generate_signature(data, private_key)

# Виведення публічного ключа та підпису
print("Generated Public Key:")
print(public_key.decode())

print("\nGenerated Signature (Base64):")
print(signature)

verify = VerifyRequest()

# Перевірка підпису
is_verified = verify.verify_signature(data, signature, public_key.decode())
if is_verified:
    print("\nПідпис вірний!")
else:
    print("\nПідпис не вірний!")
