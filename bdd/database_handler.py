import os
import sqlite3


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
        """Create all tables for the database"""

        cursor = self.conn.cursor()
        query_models = "CREATE TABLE IF NOT EXISTS Models (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                    name TEXT NOT NULL,\
                    path TEXT NOT NULL\
                    );"
        cursor.execute(query_models)

        query_textures = "CREATE TABLE IF NOT EXISTS Textures (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                    asset_id INTEGER REFERENCES Models (id) NOT NULL,\
                    type TEXT NOT NULL,\
                    path TEXT NOT NULL\
                    );"
        cursor.execute(query_textures)
        cursor.close()
        self.conn.commit()

    def close_connection(self) -> None:
        """Close database connection"""

        self.conn.close()

    def add_asset(self, name: str, path: str) -> None:
        """Add new 3D asset into the 3DModels table"""

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
