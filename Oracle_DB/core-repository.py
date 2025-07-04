# Repository Pattern Implementation

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from core.database import db

class BaseRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def create(self, entity: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def update(self, id: str, updates: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

class OracleRepository(BaseRepository):
    def __init__(self, table_name: str):
        self.table_name = table_name

    def _execute_query(self, query: str, params: tuple = None, fetch_one: bool = False):
        with db.get_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query, params or ())
                if fetch_one:
                    return cursor.fetchone()
                return cursor.fetchall()
            finally:
                cursor.close()

    def _execute_operation(self, query: str, params: tuple = None) -> bool:
        with db.get_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query, params or ())
                connection.commit()
                return cursor.rowcount > 0
            except Exception as e:
                connection.rollback()
                raise
            finally:
                cursor.close()