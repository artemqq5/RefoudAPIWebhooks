import logging

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi import Request
from fastapi.logger import logger
from fastapi.responses import Response
from pydantic import ValidationError
from starlette import status
from starlette.responses import JSONResponse

from data.repository.AccountRepository import AccountRepository
from data.transaction.RefundTransaction import RefundTransaction
from domain.notify_.NotifyAdmins import NotifyAdmins
from domain.notify_.NotifyClients import NotifyClients
from domain.request_.models import RequestDataModel
from domain.request_.verify_request import VerifyRequest
from private_config import PUBLIC_KEY

# Створюємо екземпляр FastAPI
app = FastAPI()
verify = VerifyRequest()

# Налаштовуємо формат логів
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def validate_request(request: Request, signature: str = Header(...)) -> RequestDataModel:
    try:
        body = await request.json()
        logger.info(f"Body: {body}")

        data: RequestDataModel = RequestDataModel(**body)
        logger.info(f"Signature: {signature}")

        is_verified = verify.verify_signature(data.dict(), signature, PUBLIC_KEY)

        if not is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Signature")
        return data

    except ValidationError as e:
        logger.error(f"Exception validation data: {e}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=e.errors())
    except Exception as e:
        logger.exception(f"Exception processing request: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing request")


@app.post("/mtgooglebot/refound", status_code=status.HTTP_200_OK)
async def refound(request: Request, validation: RequestDataModel = Depends(validate_request)):

    print(f"Action: {validation.action} | Success: {validation.success}")
    if validation.action != "CLOSE_ACCOUNT" or not validation.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect status of refund")

    refund_transaction = RefundTransaction().refund_transaction(validation.account)
    print(refund_transaction)

    if not refund_transaction['result']:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred during refund processing.",
        )

    account = validation.account
    await NotifyClients.push_team_refund(account.account_id, account.customer_id)
    await NotifyAdmins.push_admins_refund(account.account_id, account.customer_id)

    return Response(status_code=200)


@app.post("/mtgooglebot/created", status_code=status.HTTP_200_OK)
async def created(request: Request, validation: RequestDataModel = Depends(validate_request)):

    print(f"Action: {validation.action} | Success: {validation.success} - {validation.action}")
    account = validation.account

    if validation.action == "CREATE_BUDGET" and validation.success:
        if AccountRepository().account_by_uid(account.account_id)['budget_created']:
            logging.error("account already created budget")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="account already created budget")
        await NotifyAdmins.push_admins_create_budget(account.account_id, account.customer_id, account.balance)
        await NotifyClients.push_team_create_budget(account.account_id, account.customer_id, account.balance)

        AccountRepository().update_budget_created(account.account_id)

        return Response(status_code=200)

    if validation.action == "INVITE" and validation.success:
        if AccountRepository().account_by_uid(account.account_id)['budget_created']:
            logging.error("account already get invite")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="account already get invite")
        await NotifyAdmins.push_admins_invite(account.account_id, account.customer_id)
        await NotifyClients.push_team_invite(account.account_id, account.customer_id)

        AccountRepository().update_invite_send(account.account_id)

        return Response(status_code=200)

    if validation.action != "CREATE_ACCOUNT" or not validation.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect status")

    if AccountRepository().account_by_uid(account.account_id).get('customer_id'):
        logging.error("Customer ID already set for account")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer ID already set for account")

    update_account_id = AccountRepository().update_customer_id(
        validation.account.account_id, validation.account.customer_id
    )

    if not update_account_id:
        logging.error("Internal server error occurred during update customer_id processing.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred during update customer_id processing.",
        )
    
    await NotifyClients.push_team_verificated_account(account.account_id, account.customer_id)
    await NotifyAdmins.push_admins_verificated_account(account.account_id, account.customer_id)

    return Response(status_code=200)

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
