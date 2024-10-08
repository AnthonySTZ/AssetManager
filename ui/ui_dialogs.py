from PySide6.QtWidgets import QComboBox, QFileDialog, QDialog, QMessageBox
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
    def __init__(
        self, database: DatabaseHandler, existing_item: {}, parent=None
    ) -> None:
        super().__init__(UiImportAssetDialog, parent)
        self.database = database
        self.materials = {}  # material_id : index
        self.all_infos = {}
        self.item = existing_item
        if self.item == {}:
            self.ui.delete_btn.hide()
            self.select_file()
        else:
            self.ui.delete_btn.clicked.connect(self.delete_item)

        self.update_material()
        self.ui.file_btn.clicked.connect(self.select_file)

        if self.item != {}:
            self.update_infos()

    def update_infos(self) -> None:
        self.ui.name_te.setText(self.item["name"])
        self.ui.path_te.setText(self.item["path"])
        if self.item["material_id"] is None:
            return
        self.ui.material_cb.setCurrentIndex(self.materials[self.item["material_id"]])

    def get_file_name(self, path: str) -> str:
        last_slash = path[::-1].find("/")
        last_point = path[::-1].find(".")
        file_name = path[-last_slash : -last_point - 1]
        return file_name

    def select_file(self) -> None:
        file_path = QFileDialog.getOpenFileName(
            self,
            "Select file",
            "A:/Programming/AssetManager/",
            "(*.fbx *.obj *.abc)",
        )[0]
        if file_path:
            self.ui.path_te.setText(file_path)
            if self.ui.name_te.toPlainText() == "":
                file_name = self.get_file_name(file_path)
                self.ui.name_te.setText(file_name)

    def everything_is_correct(self) -> bool:
        if self.ui.name_te.toPlainText() == "":
            print("Please enter a valid Name")
            return False

        if self.ui.path_te.toPlainText() == "":
            print("Please enter a valid Path")
            return False

        self.get_all_infos()

        return True

    def get_all_infos(self) -> None:
        self.all_infos["name"] = self.ui.name_te.toPlainText()
        self.all_infos["path"] = self.ui.path_te.toPlainText()

        material_index = self.ui.material_cb.currentIndex()

        if material_index == 0:
            self.all_infos["material_id"] = None
        else:
            for id, index in self.materials.items():
                if index == material_index:
                    self.all_infos["material_id"] = id

    def update_material(self) -> None:
        materials = self.database.get_all_item_of_table("Materials", "")
        for i, mat in enumerate(materials):
            self.materials[mat["id"]] = i + 1  # Store material index at id
            self.ui.material_cb.addItem(mat["name"])

    def delete_item_popup(self) -> bool:
        message = QMessageBox()
        response = message.question(
            self,
            "",
            "Are you sure to delete this asset ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        return response == QMessageBox.Yes

    def delete_item(self) -> None:
        is_ok = self.delete_item_popup()
        if not is_ok:
            return

        self.database.delete_row_by_id("Models", self.item["id"])
        self.all_infos = {}
        self.close()


class ImportTextureDialog(DialogTemplate):
    def __init__(
        self, database: DatabaseHandler, existing_item: None, parent=None
    ) -> None:
        super().__init__(UiImportTextureDialog, parent)
        self.database = database
        self.ui.file_btn.clicked.connect(self.select_file)

        self.all_infos = {}
        self.item = existing_item
        if self.item == {}:
            self.ui.delete_btn.hide()
            self.select_file()
        else:
            self.ui.delete_btn.clicked.connect(self.delete_item)
            self.update_infos()

    def update_infos(self) -> None:
        self.ui.name_te.setText(self.item["name"])
        self.ui.path_te.setText(self.item["path"])

    def get_file_name(self, path: str) -> str:
        last_slash = path[::-1].find("/")
        last_point = path[::-1].find(".")
        file_name = path[-last_slash : -last_point - 1]
        return file_name

    def select_file(self) -> None:
        file_path = QFileDialog.getOpenFileName(
            self,
            "Select file",
            "A:/Programming/AssetManager/",
            "(*.exr *.jpg *.png *.tif *.tiff)",
        )[0]
        if file_path:
            self.ui.path_te.setText(file_path)
            if self.ui.name_te.toPlainText() == "":
                file_name = self.get_file_name(file_path)
                self.ui.name_te.setText(file_name)

    def everything_is_correct(self) -> bool:
        if self.ui.name_te.toPlainText() == "":
            print("Please enter a valid Name")
            return False

        if self.ui.path_te.toPlainText() == "":
            print("Please enter a valid Path")
            return False

        self.get_all_infos()

        return True

    def get_all_infos(self) -> None:
        self.all_infos["name"] = self.ui.name_te.toPlainText()
        self.all_infos["path"] = self.ui.path_te.toPlainText()

    def delete_item_popup(self) -> bool:
        message = QMessageBox()
        response = message.question(
            self,
            "",
            "Are you sure to delete this texture ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        return response == QMessageBox.Yes

    def delete_item(self) -> None:
        is_ok = self.delete_item_popup()
        if not is_ok:
            return
        self.database.delete_row_by_id("Textures", self.item["id"])
        self.all_infos = {}
        self.close()


class CreateMaterialDialog(DialogTemplate):
    def __init__(self, database, existing_item: None, parent=None) -> None:
        super().__init__(UiCreateMaterialDialog, parent)
        self.database = database

        self.textures = {}  # texture_id : index
        self.all_infos = {}
        self.item = existing_item
        self.get_all_textures()
        if self.item == {}:
            self.ui.delete_btn.hide()
        else:
            self.ui.delete_btn.clicked.connect(self.delete_item)
            self.update_infos()

    def update_infos(self) -> None:
        self.ui.name_te.setText(self.item["name"])
        if self.item["diffuse_id"] in self.textures:
            self.ui.diffuse_cb.setCurrentIndex(self.textures[self.item["diffuse_id"]])
        if self.item["specular_id"] in self.textures:
            self.ui.specular_cb.setCurrentIndex(self.textures[self.item["specular_id"]])
        if self.item["roughness_id"] in self.textures:
            self.ui.roughness_cb.setCurrentIndex(
                self.textures[self.item["roughness_id"]]
            )
        if self.item["metalness_id"] in self.textures:
            self.ui.metalness_cb.setCurrentIndex(
                self.textures[self.item["metalness_id"]]
            )
        if self.item["normal_id"] in self.textures:
            self.ui.normal_cb.setCurrentIndex(self.textures[self.item["normal_id"]])
        if self.item["displacement_id"] in self.textures:
            self.ui.displacement_cb.setCurrentIndex(
                self.textures[self.item["displacement_id"]]
            )

    def everything_is_correct(self) -> bool:
        if self.ui.name_te.toPlainText() == "":
            print("Please enter a valid Name")
            return False

        self.get_all_infos()

        return True

    def get_all_infos(self):
        self.all_infos["name"] = self.ui.name_te.toPlainText()
        self.all_infos["diffuse_id"] = self.get_texture_id(
            self.ui.diffuse_cb.currentIndex()
        )
        self.all_infos["specular_id"] = self.get_texture_id(
            self.ui.specular_cb.currentIndex()
        )
        self.all_infos["roughness_id"] = self.get_texture_id(
            self.ui.roughness_cb.currentIndex()
        )
        self.all_infos["metalness_id"] = self.get_texture_id(
            self.ui.metalness_cb.currentIndex()
        )
        self.all_infos["normal_id"] = self.get_texture_id(
            self.ui.normal_cb.currentIndex()
        )
        self.all_infos["displacement_id"] = self.get_texture_id(
            self.ui.displacement_cb.currentIndex()
        )

    def get_texture_id(self, index):
        if index == 0:
            return None
        for id, idx in self.textures.items():
            if index == idx:
                return id

        return None

    def get_all_textures(self) -> None:
        textures = self.database.get_all_item_of_table("Textures", "")
        for i, texture in enumerate(textures):
            self.textures[texture["id"]] = i + 1
            for cb in self.ui.mainFrame.findChildren(QComboBox):
                cb.addItem(texture["name"])

    def delete_item_popup(self) -> bool:
        message = QMessageBox()
        response = message.question(
            self,
            "",
            "Are you sure to delete this Material ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        return response == QMessageBox.Yes

    def delete_item(self) -> None:
        is_ok = self.delete_item_popup()
        if not is_ok:
            return
        self.database.delete_row_by_id("Materials", self.item["id"])
        self.all_infos = {}
        self.close()
