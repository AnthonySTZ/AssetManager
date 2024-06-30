import maya.cmds as cmds
import os
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QTextEdit,
    QComboBox,
    QWidget,
    QListWidgetItem,
    QListWidget,
    QAbstractItemView,
    QVBoxLayout,
    QListView,
)
from functools import partial  # optional, for passing args during signal function calls
import sys
import re
import sqlite3
import ressources_maya_rc


from maya_scripts.ui_items_maya import ItemWidget
from bdd.database_handler import DatabaseHandler


class mainWindow(QDialog):
    def __init__(self, uiRelativePath, parent=QApplication.activeWindow()):
        super(mainWindow, self).__init__(parent)
        # Load UI file
        self.init_maya_ui(uiRelativePath)
        self.ui.items_lw.horizontalScrollBar().setEnabled(False)
        self.ui.items_lw.setWrapping(True)
        self.ui.items_lw.setResizeMode(QListView.ResizeMode.Adjust)

        self.filter_type = {"Models": True, "Textures": True, "Materials": True}
        self.thumbnails_cache = {}

        self.init_buttons()

    def show_window(self) -> None:
        self.resize(890, 550)
        self.show()
        self.init_database()

    def init_maya_ui(self, uiRelativePath) -> None:
        loader = QtUiTools.QUiLoader()
        dirname = os.path.dirname(__file__)
        uiFilePath = os.path.join(dirname, uiRelativePath)
        uifile = QtCore.QFile(uiFilePath)
        uifile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uifile)
        self.centralLayout = QVBoxLayout(self)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.centralLayout.addWidget(self.ui)
        self.ui.items_lw.horizontalScrollBar().setEnabled(False)

    def init_buttons(self) -> None:
        self.ui.search_te.textChanged.connect(self.refresh_items)
        self.ui.all_check.clicked.connect(lambda: self.update_filter(True))
        self.ui.models_check.clicked.connect(lambda: self.update_filter(False))
        self.ui.textures_check.clicked.connect(lambda: self.update_filter(False))
        self.ui.materials_check.clicked.connect(lambda: self.update_filter(False))

    def init_database(self) -> None:
        self.database_handler = DatabaseHandler("assets.db")
        self.refresh_items(updateItems=True)

    def add_all_items(self) -> None:
        for item in self.items:
            if item["type"] == "Textures":
                if "texture_" + str(item["id"]) not in self.thumbnails_cache:
                    self.thumbnails_cache["texture_" + str(item["id"])] = QPixmap(
                        item["path"]
                    )
            item_widget = ItemWidget(self.database_handler, item, self.thumbnails_cache)
            item = QListWidgetItem(self.ui.items_lw)
            item.setSizeHint(item_widget.size())
            self.ui.items_lw.addItem(item)
            self.ui.items_lw.setItemWidget(item, item_widget)

    def get_all_items(self) -> list[dict]:
        search_text = self.ui.search_te.toPlainText()
        items = []
        if self.filter_type["Models"]:
            self.all_assets = self.database_handler.get_all_item_of_table(
                "Models", search_text
            )
            items += self.all_assets
        if self.filter_type["Textures"]:
            self.all_textures = self.database_handler.get_all_item_of_table(
                "Textures", search_text
            )
            items += self.all_textures
        if self.filter_type["Materials"]:
            self.all_materials = self.database_handler.get_all_item_of_table(
                "Materials", search_text
            )
            items += self.all_materials

        return items

    def closeEvent(self, event) -> None:
        self.database_handler.close_connection()

    def set_all_filter(self) -> None:
        self.filter_type["Models"] = True
        self.filter_type["Textures"] = True
        self.filter_type["Materials"] = True
        self.ui.all_check.setChecked(True)
        self.ui.models_check.setChecked(False)
        self.ui.textures_check.setChecked(False)
        self.ui.materials_check.setChecked(False)

    def update_filter(self, is_all: bool) -> None:

        if is_all:
            self.set_all_filter()

        if not is_all:
            self.ui.all_check.setChecked(False)
            self.filter_type["Models"] = self.ui.models_check.isChecked()
            self.filter_type["Textures"] = self.ui.textures_check.isChecked()
            self.filter_type["Materials"] = self.ui.materials_check.isChecked()

            if not (
                self.ui.models_check.isChecked()
                or self.ui.textures_check.isChecked()
                or self.ui.materials_check.isChecked()
            ):  # If all filter are disabled reenable the all filter
                self.set_all_filter()

        self.refresh_items()

    def refresh_items(self, updateItems=True) -> None:
        if updateItems:
            self.items = self.get_all_items()
        self.ui.items_lw.clear()
        self.add_all_items()


def openWindow():
    """
    ID Maya and attach tool window.
    """
    # Maya uses this so it should always return True
    if QApplication.instance():
        # Id any current instances of tool and destroy
        for win in QApplication.allWindows():
            if "Import" in win.objectName():  # update this name to match name below
                win.destroy()

    # QtWidgets.QApplication(sys.argv)
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
    mainWindow.window = mainWindow("ui/maya_window.ui", parent=mayaMainWindow)
    mainWindow.window.setObjectName(
        "Import"
    )  # code above uses this to ID any existing windows
    mainWindow.window.setWindowTitle("Maya Import Tool")
    mainWindow.window.show_window()
