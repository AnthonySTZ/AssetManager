"""
Constant of the SQL scripts for creating all SQL tables
"""

TABLE_MODELS = "CREATE TABLE IF NOT EXISTS Models (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                    name TEXT NOT NULL,\
                    path TEXT NOT NULL\
                    );"

TABLE_TEXTURES = "CREATE TABLE IF NOT EXISTS Textures (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                    name TEXT NOT NULL,\
                    path TEXT NOT NULL\
                    );"

TABLE_MATERIALS = "CREATE TABLE IF NOT EXISTS Materials (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                    asset_id INTEGER REFERENCES Models (id) NOT NULL,\
                    diffuse_id INTEGER REFERENCES Textures (id),\
                    specular_id INTEGER REFERENCES Textures (id),\
                    roughness_id INTEGER REFERENCES Textures (id),\
                    metalness_id INTEGER REFERENCES Textures (id),\
                    normal_id INTEGER REFERENCES Textures (id),\
                    displacement_id INTEGER REFERENCES Textures (id)\
                    );"


ALL_TABLES = [TABLE_MODELS, TABLE_TEXTURES, TABLE_MATERIALS]
