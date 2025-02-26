from data.DefaultDataBase import DefaultDataBase


class AccountRepository(DefaultDataBase):

    def update_customer_id(self, account_uid, customer_id):
        query = "UPDATE `sub_accounts` SET `customer_id` = %s WHERE `account_uid` = %s;"
        return self._update(query, (customer_id, account_uid))

    def account_by_uid(self, account_uid):
        query = "SELECT * FROM `sub_accounts` WHERE `account_uid` = %s LIMIT 1;"
        return self._select_one(query, (account_uid,))
