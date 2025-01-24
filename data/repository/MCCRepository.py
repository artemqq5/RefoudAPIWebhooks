from data.DefaultDataBase import DefaultDataBase


class MCCRepository(DefaultDataBase):
    def mcc_by_uuid(self, mcc_uuid):
        query = "SELECT * FROM `mcc` WHERE `mcc_uuid` = %s LIMIT 1;"
        return self._select_one(query, (mcc_uuid,))
