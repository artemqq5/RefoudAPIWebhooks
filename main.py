import logging

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi import Request
from fastapi.logger import logger

from domain.verify_request import VerifyRequest
from private_config import PUBLIC_KEY

# Створюємо екземпляр FastAPI
app = FastAPI()
verify = VerifyRequest()

# Налаштовуємо формат логів
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат логів
    handlers=[
        logging.StreamHandler()  # Виводить логи в консоль
    ]
)


# Функція для логування запиту
async def log_request(request: Request):
    try:
        body = await request.json()
        logger.info(f"Тіло запиту: {body}")
    except Exception as e:
        logger.error(f"Не вдалося зчитати тіло запиту: {e}")


# Функція для валідації запиту
async def validate_request(request: Request, signature: str = Header(...)):
    await log_request(request)
    data_dict = await request.json()
    logger.info(f"Отриманий підпис: {signature}")

    is_verified = verify.verify_signature(data_dict, signature, PUBLIC_KEY)

    if not is_verified:
        raise HTTPException(status_code=400, detail="Невірний підпис")


# Основний маршрут
@app.post("/mtgooglebot/refound")
async def refound(request: Request, validation: dict = Depends(validate_request)):
    logger.info("Запит успішний")
    return {"state": "success"}


@app.get("/mtgooglebot/refound")
async def refound(request: Request, validation: dict = Depends(validate_request)):
    logger.info("Це Get запит (навіщо він тут взагалі) !!!!!!!")
    return {"state": "error", "message": "Only post requests"}

#
#  ==========================================================
#  DATA EXAMPLE
#  ==========================================================
# {
#     'account': {
#         'account_id': 'db5ee78a-e9e6-47c3-9df9-9572ecf6735e',
#         'balance': '140.52',
#         'currency': 'USD',
#         'customer_id': '6406938403',
#         'email': 'denversmilla@gmail.com',
#         'limit': '0.00',
#         'spend': '0.00',
#         'status': 'CLOSED'
#     },
#     'action': 'CLOSE_ACCOUNT',
#     'exception': '',
#     'success': True,
#     'uid': 'fcfcba60-b722-4171-8d7b-6e8d021861d8'
# }
