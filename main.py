"""
"""

from bdd.database_handler import DatabaseHandler

database_handler = DatabaseHandler("assets.db")


def add_asset():
    print("---ADD ASSET---")
    asset_name = input("\nAsset Name : ")
    asset_path = input("\nAsset Path : ")

    database_handler.add_asset(asset_name, asset_path)


add_asset()

database_handler.close_connection()
