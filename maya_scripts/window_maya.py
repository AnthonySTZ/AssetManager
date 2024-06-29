import maya.cmds as cmds
import os
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore
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

        self.filter_type = {"Models": True, "Textures": True, "Materials": True}

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
            self.add_item(item)

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

    def add_item_to_listWidget(self, list_widget, widget) -> None:
        item = QListWidgetItem(list_widget)
        item.setSizeHint(widget.size())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, widget)

    def add_item_row(self, item) -> None:
        list_widget = QListWidget()
        list_widget.setFlow(QListWidget.LeftToRight)
        # list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        list_widget.horizontalScrollBar().setEnabled(False)
        list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        list_widget.setFixedSize(
            self.ui.items_lw.width(), ItemWidget(self.database_handler).height() + 10
        )
        self.add_item_to_listWidget(self.ui.items_lw, list_widget)

    def is_item_row_full(self):

        last_row_item = self.ui.items_lw.item(self.ui.items_lw.count() - 1)
        last_row = self.ui.items_lw.itemWidget(last_row_item)
        last_row_item_nb = last_row.count()
        widget_width = ItemWidget(self.database_handler).width()
        return (last_row_item_nb + 1) * widget_width > self.ui.items_lw.width()

    def add_item(self, item) -> None:
        if self.ui.items_lw.count() == 0:
            self.add_item_row(item)

        elif self.is_item_row_full():
            self.add_item_row(item)

        item_widget = ItemWidget(self.database_handler, item)
        last_row_item = self.ui.items_lw.item(self.ui.items_lw.count() - 1)
        self.add_item_to_listWidget(
            self.ui.items_lw.itemWidget(last_row_item), item_widget
        )

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

    def resizeEvent(self, event) -> None:
        QDialog.resizeEvent(self, event)
        try:  # Check if resize is called before the window is created
            self.refresh_items()
        except AttributeError:
            pass


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
