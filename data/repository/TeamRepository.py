from data.DefaultDataBase import DefaultDataBase


class TeamRepository(DefaultDataBase):

    def team_users_by_uuid(self, team_uuid):
        query = "SELECT * FROM `access` WHERE `team_uuid` = %s AND `user_id` IS NOT NULL;"
        return self._select(query, (team_uuid,))

