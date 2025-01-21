from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.logger import logger

from domain.verify_request import VerifyRequest
from private_config import PUBLIC_KEY
from fastapi import Request

app = FastAPI()
verify = VerifyRequest()

import logging
logging.basicConfig(level=logging.INFO)


async def log_request(request: Request):
    # Логування інформації про запит
    logger.info(f"Запит: {request.method} {request.url}")
    logger.info(f"Хедери: {dict(request.headers)}")

    # Параметри запиту
    query_params = dict(request.query_params)
    if query_params:
        logger.info(f"Параметри запиту: {query_params}")

    # Тіло запиту
    try:
        body = await request.json()
        logger.info(f"Тіло запиту: {body}")
    except Exception as e:
        logger.error(f"Не вдалося зчитати тіло запиту: {e}")


async def validate_request(request: Request, signature: str = Header(...)):
    await log_request(request)
    data_dict = await request.json()
    logger.info(signature)
    is_verified = verify.verify_signature(data_dict, signature, PUBLIC_KEY)

    if not is_verified:
        raise HTTPException(status_code=400, detail="Невірний підпис")


@app.post("/mtgooglebot/refound")
async def refound(request: Request, validation: dict = Depends(validate_request)):
    logger.info("Запит успішний")
    return {"state": "success"}
