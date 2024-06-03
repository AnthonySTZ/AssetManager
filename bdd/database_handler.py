import os
import sqlite3
from bdd.databaseDDL import ALL_TABLES


class DatabaseHandler:
    def __init__(self, database_name: str) -> None:
        """Initialize database connection"""

        self.conn = sqlite3.connect(
            f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}"
        )

        self.create_database()  # Create Database tables if not exists

        self.conn.row_factory = (
            sqlite3.Row
        )  # Set default return to Dictionnary instead of List

    def create_database(self) -> None:
        """Create all tables needed for the database"""

        cursor = self.conn.cursor()

        for table in ALL_TABLES:
            query = table
            cursor.execute(query)

        cursor.close()
        self.conn.commit()

    def close_connection(self) -> None:
        """Close database connection"""

        self.conn.close()

    def add_asset(self, name: str, path: str) -> None:
        """Add new 3D asset into the 3DModels table"""

        if not name:  # Check if name is None or empty
            print("Please use a valid Name")
            return

        if not path:  # Check if name is None or empty
            print("Please use a valid Path")
            return

        cursor = self.conn.cursor()
        query = "INSERT INTO Models (name, path) VALUES (?, ?)"
        cursor.execute(
            query,
            (
                name,
                path,
            ),
        )
        cursor.close()
        self.conn.commit()
