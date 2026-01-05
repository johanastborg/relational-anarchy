from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd

class RDBMSInterface(ABC):
    @abstractmethod
    def fetch_table_schema(self, table_name: str) -> str:
        """Returns the schema of the table."""
        pass

    @abstractmethod
    def fetch_data(self, table_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetches data from the table."""
        pass

    @abstractmethod
    def list_tables(self) -> List[str]:
        """Lists all tables in the database."""
        pass

class MockRDBMS(RDBMSInterface):
    def __init__(self):
        self.data = {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
                {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
                {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"},
            ],
            "orders": [
                {"order_id": 101, "user_id": 1, "product": "Laptop", "amount": 1200},
                {"order_id": 102, "user_id": 2, "product": "Phone", "amount": 800},
                {"order_id": 103, "user_id": 1, "product": "Monitor", "amount": 300},
            ]
        }
        self.schemas = {
            "users": "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR, email VARCHAR, role VARCHAR)",
            "orders": "CREATE TABLE orders (order_id INT PRIMARY KEY, user_id INT, product VARCHAR, amount INT, FOREIGN KEY (user_id) REFERENCES users(id))"
        }

    def fetch_table_schema(self, table_name: str) -> str:
        return self.schemas.get(table_name, "")

    def fetch_data(self, table_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        return self.data.get(table_name, [])[:limit]

    def list_tables(self) -> List[str]:
        return list(self.data.keys())
