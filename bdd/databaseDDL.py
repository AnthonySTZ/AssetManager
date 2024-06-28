"""
Constants SQL scripts for creating all SQL tables
"""

TABLE_MODELS = "CREATE TABLE IF NOT EXISTS Models (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                    name TEXT NOT NULL,\
                    path TEXT NOT NULL,\
                    material_id INTERGER REFERENCES Materials (id) ON DELETE SET NULL\
                    );"

TABLE_TEXTURES = "CREATE TABLE IF NOT EXISTS Textures (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                    name TEXT NOT NULL UNIQUE,\
                    path TEXT NOT NULL\
                    );"

TABLE_MATERIALS = "CREATE TABLE IF NOT EXISTS Materials (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                    name TEXT NOT NULL,\
                    diffuse_id INTEGER REFERENCES Textures (id) ON DELETE SET NULL,\
                    specular_id INTEGER REFERENCES Textures (id) ON DELETE SET NULL,\
                    roughness_id INTEGER REFERENCES Textures (id) ON DELETE SET NULL,\
                    metalness_id INTEGER REFERENCES Textures (id) ON DELETE SET NULL,\
                    normal_id INTEGER REFERENCES Textures (id) ON DELETE SET NULL,\
                    displacement_id INTEGER REFERENCES Textures (id) ON DELETE SET NULL\
                    );"

ALL_TABLES = [TABLE_MODELS, TABLE_TEXTURES, TABLE_MATERIALS]
