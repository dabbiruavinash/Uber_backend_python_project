# Database Connection Manager

import cx_Oracle
from contextlib import contextmanager
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class OracleDB:
    def __init__(self):
        self.connection_pool = None
        self._create_pool()

    def _create_pool(self):
        try:
            self.connection_pool = cx_Oracle.SessionPool(
                user=settings.ORACLE_USER,
                password=settings.ORACLE_PASSWORD,
                dsn=settings.ORACLE_DSN,
                min=1,
                max=10,
                increment=1,
                threaded=True,
                encoding="UTF-8"
            )
            logger.info("Oracle connection pool created successfully")
        except cx_Oracle.DatabaseError as e:
            logger.error(f"Failed to create Oracle connection pool: {str(e)}")
            raise

    @contextmanager
    def get_connection(self):
        connection = None
        try:
            connection = self.connection_pool.acquire()
            yield connection
        except cx_Oracle.DatabaseError as e:
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            if connection:
                self.connection_pool.release(connection)

    def close_pool(self):
        if self.connection_pool:
            self.connection_pool.close()
            logger.info("Oracle connection pool closed")

# Singleton instance
db = OracleDB()