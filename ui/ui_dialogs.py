from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QFileDialog, QDialog
from ui.ui_setups.ui_import_asset import Ui_Dialog as UiImportAssetDialog
from ui.ui_setups.ui_import_texture import Ui_Dialog as UiImportTextureDialog
from ui.ui_setups.ui_create_material import Ui_Dialog as UiCreateMaterialDialog

import os
from bdd.database_handler import DatabaseHandler


class DialogTemplate(QDialog):
    def __init__(self, ui, parent=None) -> None:
        super().__init__(parent)
        self.ui = ui()
        self.ui.setupUi(self)

        self.status = False
        self.init_buttons()

    def init_buttons(self) -> None:
        self.ui.accept_btn.clicked.connect(self.accept_event)
        self.ui.cancel_btn.clicked.connect(self.cancel_event)

    def everything_is_correct(self) -> bool:
        return False

    def accept_event(self) -> None:
        if not self.everything_is_correct():
            return
        self.status = True
        self.close()

    def cancel_event(self) -> None:
        self.close()


class ImportAssetDialog(DialogTemplate):
    def __init__(self, database: DatabaseHandler, parent=None) -> None:
        super().__init__(UiImportAssetDialog, parent)
        self.database = database

        self.update_material()
        self.ui.file_btn.clicked.connect(self.select_file)

    def select_file(self) -> None:
        file_path = QFileDialog.getOpenFileName(
            self,
            "Select file",
            "/home/boby/Documents/Projects/AssetManager/",
            "(*.fbx *.obj *.abc)",
        )[0]
        if file_path:
            self.ui.path_te.setText(file_path)

    def everything_is_correct(self) -> bool:
        if self.ui.name_te.toPlainText() == "":
            print("Please enter a valid Name")
            return False

        if self.ui.path_te.toPlainText() == "":
            print("Please enter a valid Path")
            return False

        if not os.path.exists(self.ui.path_te.toPlainText()):
            print("Path not exists")
            return False

        if self.path_already_exist():
            print("Path already exists")
            return False

        return True

    def update_material(self) -> None:
        materials = self.database.get_all_item_of_table("Materials")
        for mat in materials:
            self.ui.material_cb.addItem(mat["name"])

    def path_already_exist(self) -> bool:
        assets = self.database.get_all_item_of_table("Models")
        path = self.ui.path_te.toPlainText()
        for item in assets:
            if item["path"] == path:
                return True

        return False


class ImportTextureDialog(DialogTemplate):
    def __init__(self, database, parent=None) -> None:
        super().__init__(UiImportTextureDialog, parent)
        self.database = database

    def everything_is_correct(self) -> bool:
        if self.ui.name_te.toPlainText() == "":
            print("Please enter a valid Name")
            return False

        if self.ui.path_te.toPlainText() == "":
            print("Please enter a valid Path")
            return False

        if self.path_already_exist():
            print("Path already exists")
            return False

        return True

    def path_already_exist(self) -> bool:
        textures = self.database.get_all_item_of_table("Textures")
        path = self.ui.path_te.toPlainText()
        for item in textures:
            if item["path"] == path:
                return True

        return False


class CreateMaterialDialog(DialogTemplate):
    def __init__(self, database, parent=None) -> None:
        super().__init__(UiCreateMaterialDialog, parent)
        self.database = database
        self.get_all_textures()

    def everything_is_correct(self) -> bool:
        if self.ui.name_te.toPlainText() == "":
            print("Please enter a valid Name")
            return False

        return True

    def get_all_textures(self) -> None:
        textures = self.database.get_all_item_of_table("Textures")
        for texture in textures:
            for cb in self.ui.mainFrame.findChildren(QComboBox):
                cb.addItem(texture["name"])
