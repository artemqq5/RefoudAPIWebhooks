from asyncio.log import logger

import pymysql

from private_config import DATABASE_PASSWORD, DATABASE_NAME


class DefaultDataBase:
    def __init__(self, con_transaction=None):
        self._connection_tran = con_transaction or pymysql.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            db=DATABASE_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )

    def _insert(self, query, args=None):
        try:
            with self._connection_tran.cursor() as cursor:
                result = cursor.execute(query, args)
                return result
        except Exception as e:
            logger.error(f"_insert: {e}")
            self._connection_tran.rollback()

    def _update(self, query, args=None):
        try:
            with self._connection_tran.cursor() as cursor:
                result = cursor.execute(query, args)
                return result
        except Exception as e:
            logger.error(f"_update: {e}")
            self._connection_tran.rollback()

    def _delete(self, query, args=None):
        try:
            with self._connection_tran.cursor() as cursor:
                result = cursor.execute(query, args)
                return result
        except Exception as e:
            logger.error(f"_delete: {e}")
            self._connection_tran.rollback()

    def _select_one(self, query, args=None):
        try:
            with self._connection_tran.cursor() as cursor:
                cursor.execute(query, args)
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"_select_one: {e}")

    def _select(self, query, args=None):
        try:
            with self._connection_tran.cursor() as cursor:
                cursor.execute(query, args)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"_select_all: {e}")

    def _begin_transaction(self):
        try:
            self._connection_tran.begin()
        except Exception as e:
            logger.error(f"begin_transaction: {e}")
            raise

    def _commit(self):
        """Коміт транзакції."""
        try:
            self._connection_tran.commit()
        except Exception as e:
            logger.error(f"commit: {e}")
            self._connection_tran.rollback()

    def _rollback(self):
        """Відкат транзакції."""
        try:
            self._connection_tran.rollback()
        except Exception as e:
            logger.error(f"rollback: {e}")

    def _close(self):
        """Закриває з'єднання з базою даних."""
        try:
            self._connection_tran.close()
        except Exception as e:
            logger.error(f"close: {e}")
