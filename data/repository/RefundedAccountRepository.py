from data.DefaultDataBase import DefaultDataBase


class RefundedAccountRepository(DefaultDataBase):

    def account_by_uid(self, uid):
        query = "SELECT * FROM `refunded_accounts` WHERE `account_uid` = %s LIMIT 1;"
        return self._select_one(query, (uid,))
