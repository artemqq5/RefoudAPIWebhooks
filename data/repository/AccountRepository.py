from data.DefaultDataBase import DefaultDataBase


class AccountRepository(DefaultDataBase):

    def update_customer_id(self, account_uid, customer_id):
        query = "UPDATE `sub_account` SET `customer_id` = %s WHERE `account_uid` = %s;"
        return self._update(query, (customer_id, account_uid))
