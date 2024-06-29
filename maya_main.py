import sys
import maya.cmds as cmds

PLUGIN_PATH = "A:\\Programming\\AssetManager\\"
sys.path.insert(0, PLUGIN_PATH)

from importlib import reload
import maya_scripts.window_maya as window_maya
import bdd.database_handler as db
import maya_scripts.ui_items_maya as ui_items

reload(ui_items)
reload(db)
reload(window_maya)
window_maya.openWindow()
