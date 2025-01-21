import logging
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.logger import logger
from domain.verify_request import VerifyRequest
from private_config import PUBLIC_KEY
from fastapi import Request

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
    logger.info(f"Header: {dict(request.headers)}")

    query_params = dict(request.query_params)
    if query_params:
        logger.info(f"Параметри запиту: {query_params}")

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
