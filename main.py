from fastapi import FastAPI, HTTPException, Header
from requests import Request

from domain.verify_request import VerifyRequest
from private_config import PUBLIC_KEY

app = FastAPI()
verify = VerifyRequest()


@app.post("/googlebot/webhooks")
async def validate_account(request: Request, signature: str = Header(...)):
    data_dict = await request.json()

    is_verified = verify.verify_signature(data_dict, signature, PUBLIC_KEY)

    if not is_verified:
        raise HTTPException(status_code=400, detail="Невірний підпис")

    return {"status": "success", "message": "Підпис перевірено успішно"}
