from data.TransactionDataBase import TransactionDataBase


class RefundRepositoryTransaction(TransactionDataBase):

    def _ref_account_by_uid(self, account_uid):
        query = "SELECT * FROM `refunded_accounts` WHERE `account_uid` = %s LIMIT 1 FOR UPDATE;"
        return self._select_one(query, (account_uid,))

    def _update_status_refunded(self, account_uid, refunded_value, last_spend, commission):
        query = ("UPDATE `refunded_accounts` "
                 "SET `refund_value` = %s, `last_spend` = %s, `commission` = %s, `status` = 'success', `completed_time` = CURRENT_TIMESTAMP "
                 "WHERE `account_uid` = %s;")
        return self._update(query, (refunded_value, last_spend, commission, account_uid))

    def _add_value_balance(self, value, mcc_uuid, team_uuid):
        query = "UPDATE `balances` SET `balance` = `balance` + %s  WHERE `mcc_uuid` = %s AND `team_uuid` = %s;"
        return self._update(query, (value, mcc_uuid, team_uuid))
