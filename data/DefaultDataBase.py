from asyncio.log import logger

import pymysql

from private_config import DATABASE_PASSWORD, DATABASE_NAME


class DefaultDataBase:
    def __init__(self):
        self.__connection = pymysql.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            db=DATABASE_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def _insert(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    result = cursor.execute(query, args)
                    return result
        except Exception as e:
            logger.error(f"_insert: {e}")
            logger.error(f"query: {query}")

    def _update(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    result = cursor.execute(query, args)
                    return result
        except Exception as e:
            logger.error(f"_update: {e}")
            logger.error(f"query: {query}")

    def _delete(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    result = cursor.execute(query, args)
                    return result
        except Exception as e:
            logger.error(f"_delete: {e}")
            logger.error(f"query: {query}")

    def _select_one(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    cursor.execute(query, args)
                    return cursor.fetchone()
        except Exception as e:
            logger.error(f"_select_one: {e}")
            logger.error(f"query: {query}")

    def _select(self, query, args=None):
        try:
            with self.__connection as con:
                with con.cursor() as cursor:
                    cursor.execute(query, args)
                    return cursor.fetchall()
        except Exception as e:
            logger.error(f"_select_all: {e}")
            logger.error(f"query: {query}")
