"""
Handler for the files database
"""

import os
import sqlite3
from bdd.databaseDDL import ALL_TABLES


class DatabaseHandler:
    def __init__(self, database_name: str) -> None:
        """Initialize database connection"""

        self.conn = sqlite3.connect(
            os.path.dirname(os.path.abspath(__file__)) + "/" + database_name
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

    def get_all_item_of_table(self, table: str, search_text: str) -> list:
        cursor = self.conn.cursor()
        query = "SELECT * FROM " + table + ";"
        if search_text != "":
            query = (
                "SELECT * FROM " + table + " WHERE name LIKE '%" + search_text + "%';"
            )

        cursor.execute(query)
        response = cursor.fetchall()
        cursor.close()
        response = list(map(dict, response))
        for item in response:
            item["type"] = table
        return response
