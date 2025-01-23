from typing import Optional

from pydantic import BaseModel


class AccountModel(BaseModel):
    account_id: str
    balance: str
    currency: str
    customer_id: str
    email: str
    limit: str
    spend: str
    status: str


class RequestDataModel(BaseModel):
    account: AccountModel
    action: str
    exception: Optional[str] = ""
    success: bool
    uid: str
