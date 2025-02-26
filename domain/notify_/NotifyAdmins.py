import logging
from asyncio import gather

import aiohttp
from aiohttp import ClientSession

from data.repository.AccountRepository import AccountRepository
from data.repository.MCCRepository import MCCRepository
from data.repository.RefundedAccountRepository import RefundedAccountRepository
from data.repository.UserRepository import UserRepository
from domain.notify_.localization import get_message
from private_config import BOT_TOKEN

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


class NotifyAdmins:
    @staticmethod
    async def push_admins_refund(account_uid):
        counter = 0
        other = 0

        account = RefundedAccountRepository().account_by_uid(account_uid)

        admins = UserRepository().admins()
        mcc = MCCRepository().mcc_by_uuid(account['mcc_uuid'])

        async def notify_admin(admin, clsession: ClientSession):
            nonlocal counter, other
            try:
                message = get_message(
                    language=admin.get('lang', 'en'),
                    key="REFUND-ADMIN",

                    account_email=account['account_email'],
                    team_name=account['team_name'],
                    mcc_name=mcc['mcc_name'],
                    spend=account['last_spend'],
                    refund_value=account['refund_value'],
                    commission=account['commission']
                )

                payload = {
                    "chat_id": admin['user_id'],
                    "text": message,
                    "parse_mode": "HTML"
                }
                async with clsession.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        data=payload
                ) as response:
                    if response.status == 200:
                        counter += 1
                    else:
                        other += 1
                        logging.error(
                            f"Failed to send message to admin({admin['user_id']}), error: {response.status}")

            except Exception as e:
                other += 1
                logging.error(f"Admin ({admin['user_id']}) | push_admins_refund: {e}")

        async with aiohttp.ClientSession() as session:
            tasks = [notify_admin(admin, session) for admin in admins]
            await gather(*tasks)

        logging.info(f"Messaging status: {counter}/{len(admins)}\nOther errors: {other}")

    @staticmethod
    async def push_admins_verificated_account(account_uid, account_balance, customer_id):
        counter = 0
        other = 0

        account = AccountRepository().account_by_uid(account_uid)

        admins = UserRepository().admins()
        mcc = MCCRepository().mcc_by_uuid(account['mcc_uuid'])

        async def notify_admin(admin, clsession: ClientSession):
            nonlocal counter, other
            try:
                message = get_message(
                    language=admin.get('lang', 'en'),
                    key="VERIFICATED-ACCOUNT-ADMIN",

                    account_email=account['account_email'],
                    amount=account_balance,
                    mcc_name=mcc['mcc_name'],
                    team_name=account['team_name'],
                    customer_id=customer_id,
                )

                payload = {
                    "chat_id": admin['user_id'],
                    "text": message,
                    "parse_mode": "HTML"
                }
                async with clsession.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        data=payload
                ) as response:
                    if response.status == 200:
                        counter += 1
                    else:
                        other += 1
                        logging.error(
                            f"Failed to send message to admin({admin['user_id']}), error: {response.status}")

            except Exception as e:
                other += 1
                logging.error(f"Admin ({admin['user_id']}) | push_admins_verificated_account: {e}")

        async with aiohttp.ClientSession() as session:
            tasks = [notify_admin(admin, session) for admin in admins]
            await gather(*tasks)

        logging.info(f"Messaging status: {counter}/{len(admins)}\nOther errors: {other}")
