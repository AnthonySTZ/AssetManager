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

        query = "PRAGMA foreign_keys=off;"
        for table in ALL_TABLES:
            query += table
        query += "PRAGMA foreign_keys=on;"

        cursor.executescript(query)
        self.conn.commit()
        cursor.close()

    def close_connection(self) -> None:
        """Close database connection"""

        self.conn.close()

    def insert_new_row(self, table: str, datas: dict) -> int:
        """Insert datas in table"""

        # datas = {"name": "Nom", "path": "/home/blabla"}

        data_names = "(" + ", ".join(datas.keys()) + ")"  # Ex: (name, path)
        datas_column = "(" + ",".join(["?" for i in datas.keys()]) + ")"  # Ex: (?, ?)

        cursor = self.conn.cursor()
        query = (
            "INSERT INTO " + table + " " + data_names + " VALUES " + datas_column + ";"
        )
        cursor.execute(query, tuple(datas.values()))
        id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return id

    def show_all_rows(self, table: str) -> None:
        """Print all rows for a given table"""

        cursor = self.conn.cursor()
        query = "SELECT * FROM " + table + ";"
        cursor.execute(query)
        response = cursor.fetchall()

        print("---" + table + " TABLE---")
        if len(response) == 0:
            print("Nothing here :)")

        response = map(dict, response)
        for row in response:
            print(row)
        print("------\n")

    def add_asset(self, name: str, path: str) -> None:
        """Add new 3D asset into the Models table"""

        row_properties = {"name": name, "path": path}
        asset_id = self.insert_new_row("Models", row_properties)
        return asset_id

    def add_texture(self, name: str, path: str) -> None:
        """Add new texture into the Textures table"""

        row_properties = {"name": name, "path": path}
        self.insert_new_row("Textures", row_properties)

    def add_materials(self, name: str, maps: dict) -> None:
        """Add new Material into the Materials table"""

        row_properties = {"name": name}
        for key, tex in maps.items():
            if tex is not None:
                row_properties[key] = tex

        self.insert_new_row("Materials", row_properties)

    def link_material(self, asset_id: int, material_id: int) -> None:

        cursor = self.conn.cursor()
        query = "UPDATE Models SET material_id = ? WHERE id = ?;"
        cursor.execute(
            query,
            (
                material_id,
                asset_id,
            ),
        )
        cursor.close()
        self.conn.commit()

    def update_model(
        self, asset_id: int, name: str, path: str, material_id: int
    ) -> None:
        cursor = self.conn.cursor()
        if material_id is not None:
            query = (
                "UPDATE Models SET name = ?, path = ?, material_id = ? WHERE id = ?;"
            )
            cursor.execute(
                query,
                (
                    name,
                    path,
                    material_id,
                    asset_id,
                ),
            )
        else:
            query = "UPDATE Models SET name = ?, path = ? WHERE id = ?;"
            cursor.execute(
                query,
                (
                    name,
                    path,
                    asset_id,
                ),
            )

        cursor.close()
        self.conn.commit()

    def update_texture(self, texture_id: int, name: str, path: str) -> None:
        cursor = self.conn.cursor()
        query = "UPDATE Textures SET name = ?, path = ? WHERE id = ?;"
        cursor.execute(
            query,
            (
                name,
                path,
                texture_id,
            ),
        )

        cursor.close()
        self.conn.commit()

    def update_material(self, material_id: int, name: str, maps_dict: dict) -> None:

        maps = " = ?, ".join(maps_dict.keys()) + " = ?"

        cursor = self.conn.cursor()
        query = "UPDATE Materials SET name = ?, " + maps + " WHERE id = ?;"
        cursor.execute(query, (name,) + tuple(maps_dict.values()) + (material_id,))

        cursor.close()
        self.conn.commit()

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

    def delete_row_by_id(self, table: str, id: int) -> None:
        cursor = self.conn.cursor()

        query = "DELETE FROM " + table + " WHERE id = ?;"
        cursor.execute(query, (id,))
        cursor.close()
        self.conn.commit()

    def get_item_of_table_by_id(self, table: str, id: int) -> dict:
        cursor = self.conn.cursor()
        query = "SELECT * FROM " + table + " WHERE id = " + str(id) + ";"
        cursor.execute(query)
        response = cursor.fetchall()
        cursor.close()
        response = list(map(dict, response))[0]
        return response
