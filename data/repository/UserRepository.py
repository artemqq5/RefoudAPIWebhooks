from data.DefaultDataBase import DefaultDataBase


class UserRepository(DefaultDataBase):

    def admins(self):
        query = "SELECT * FROM `users` WHERE `role` = %s;"
        return self._select(query, 'admin')

