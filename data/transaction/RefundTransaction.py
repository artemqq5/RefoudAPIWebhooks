import logging

from data.repository.RefundRepositoryTransaction import RefundRepositoryTransaction
from domain.request_.models import AccountModel


class RefundTransaction(RefundRepositoryTransaction):

    def refund_transaction(self, account: AccountModel) -> dict:
        """Processes a refund transaction for an account."""

        try:
            logging.info("Starting refund transaction")
            self._begin_transaction()

            account_uid = account.account_id

            logging.info("Check if account exists")
            refunded_account = self._ref_account_by_uid(account_uid=account_uid)
            if not refunded_account:
                logging.error("Account is not found in `refunded_accounts`")
                return {"result": False, "error": "Account not found"}

            logging.info("Check if account status is not already 'success'")
            if refunded_account['status'] == 'success':
                logging.warning("Account already has (success) status in database")
                return {"result": False, "error": "Account already refunded"}

            balance = float(account.balance)
            spend = float(account.spend)
            refunded_amount = round(balance * 0.96, 3)
            commission_amount = round(balance - refunded_amount, 3)
            logging.info(
                f"Refunded amount ({balance}): {refunded_amount} with commission {commission_amount}. Spend {spend}")

            logging.info("Update account status")
            if not self._update_status_refunded(
                    account_uid=account_uid, refunded_value=refunded_amount, commission=commission_amount):
                raise Exception("Can't update status for Account in `refunded_accounts`")

            logging.info(f"Add balance reminding to MCC ({refunded_account['mcc_uuid']}) balance with commission "
                         f"| team name ({refunded_account['team_name']})")
            if refunded_amount <= 0:
                logging.info(f"Refund amount is {refunded_amount}, commission {commission_amount} skipped adding")
            else:
                if not self._add_value_balance(value=refunded_amount, mcc_uuid=refunded_account['mcc_uuid'],
                                               team_uuid=refunded_account['team_uuid']):
                    raise Exception("Unable to add balance to MCC database")

            self._commit()
            logging.info("Refund transaction completed successfully")
            return {"result": True, "account": refunded_account}

        except Exception as e:
            self._rollback()
            logging.error(f"Refund transaction failed: {e}")
            return {"result": False, "error": str(e)}
        finally:
            self._close()
            logging.info("Transaction connection closed")

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
