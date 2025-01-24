from data.TransactionDataBase import TransactionDataBase


class RefundRepositoryTransaction(TransactionDataBase):

    def _ref_account_by_uid(self, account_uid):
        query = "SELECT * FROM `refunded_accounts` WHERE `account_uid` = %s LIMIT 1 FOR UPDATE;"
        return self._select_one(query, (account_uid,))

    def _update_status_refunded(self, account_uid, refunded_value, commission, last_spend):
        query = "UPDATE `refunded_accounts` SET `refund_value` = %s, `commission` = %s, `last_spend` = %s, `status` = 'success' WHERE `account_uid` = %s;"
        return self._update(query, (refunded_value, commission, last_spend, account_uid))

    def _add_value_balance(self, value, mcc_uuid, team_uuid):
        query = "UPDATE `balances` SET `balance` = `balance` + %s  WHERE `mcc_uuid` = %s AND `team_uuid` = %s;"
        return self._update(query, (value, mcc_uuid, team_uuid))
