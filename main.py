"""
"""

from bdd.database_handler import DatabaseHandler

database_handler = DatabaseHandler("assets.db")


def add_asset():
    print("---ADD ASSET---")
    asset_name = input("\nAsset Name : ")
    asset_path = input("\nAsset Path : ")

    database_handler.add_asset(asset_name, asset_path)


def add_texture():
    print("---ADD TEXTURE---")
    texture_name = input("\nTexture Name : ")
    if not texture_name:  # Check if name is None or empty
        print("Please use a valid Name")
        return

    texture_path = input("\nTexture Path : ")
    if not texture_path:
        print("Please use a valid Path")
        return

    database_handler.add_texture(texture_name, texture_path)


def add_material():
    map_dict = {
        "diffuse_id": None,
        "specular_id": None,
        "roughness_id": None,
        "metalness_id": None,
        "normal_id": None,
        "displacement_id": None,
    }

    print("---ADD MATERIAL---")
    material_name = input("\nMaterial Name : ")
    if not material_name:
        print("Please use a valid Name")
        return

    database_handler.show_all_rows("Textures")
    for tex in map_dict.keys():
        texture_id = input(f"{tex} : ")
        if not texture_id.isnumeric():
            continue
        map_dict[tex] = int(texture_id)

    database_handler.add_materials(name=material_name, maps=map_dict)


def link_material():
    print("---LINK MATERIAL---\n")
    database_handler.show_all_rows("Models")
    asset_id = int(input("\nModel_id : "))
    database_handler.show_all_rows("Materials")
    material_id = int(input("\nMaterial_id : "))

    database_handler.link_material(asset_id=asset_id, material_id=material_id)


link_material()

database_handler.close_connection()
