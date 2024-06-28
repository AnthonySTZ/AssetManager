from PySide2.QtWidgets import QWidget, QTextEdit, QComboBox
from PySide2.QtGui import QPixmap
from maya_scripts.ui.ui_item_widget import Ui_Form as UiItemWidget
from bdd.database_handler_maya import DatabaseHandler
import os
import ressources_maya_rc


class ItemWidget(QWidget):
    def __init__(self, database: DatabaseHandler, item=None) -> None:
        super().__init__()
        self.ui = UiItemWidget()
        self.ui.setupUi(self)
        self.database = database

        self.item = item
        self.init_texts()

    def init_texts(self) -> None:
        if self.item is None:
            return

        self.ui.type_l.setText(self.item["type"])
        self.ui.name_l.setText(self.item["name"])

        self.init_type()

    def init_type(self) -> None:
        if self.item["type"] == "Models":
            self.ui.type_l.setStyleSheet("background-color: rgb(100, 0, 0);")
            self.set_icon("model")
        elif self.item["type"] == "Materials":
            self.ui.type_l.setStyleSheet("background-color: rgb(0, 100, 0);")
            self.set_icon("material")
        else:
            self.ui.type_l.setStyleSheet("background-color: rgb(0, 0, 100);")
            self.set_icon("texture")

    def set_icon(self, icon_name) -> None:
        if "path" in self.item:
            if not os.path.exists(self.item["path"]):
                icon_name = "error"
        icon = QPixmap(":/icons/ui/ressources/" + icon_name + ".png")
        self.ui.img_l.setPixmap(icon)

    """def mouseReleaseEvent(self, event) -> None:
        if self.item is None:
            return

        if self.item["type"] == "Models":
            asset_infos = self.show_dialog(ImportAssetDialog, self.item)
            if asset_infos == {}:
                return

            asset_infos["id"] = self.item["id"]
            asset_infos["type"] = self.item["type"]
            self.item = asset_infos.copy()

            self.database.update_model(
                self.item["id"],
                self.item["name"],
                self.item["path"],
                self.item["material_id"],
            )

        elif self.item["type"] == "Textures":
            texture_infos = self.show_dialog(ImportTextureDialog, self.item)
            if texture_infos == {}:
                return

            texture_infos["id"] = self.item["id"]
            texture_infos["type"] = self.item["type"]
            self.item = texture_infos.copy()

            self.database.update_texture(
                self.item["id"], self.item["name"], self.item["path"]
            )

        elif self.item["type"] == "Materials":
            material_infos = self.show_dialog(CreateMaterialDialog, self.item)
            if material_infos == {}:
                return

            material_infos["id"] = self.item["id"]
            material_infos["type"] = self.item["type"]

            self.item = material_infos.copy()
            del material_infos["id"]
            del material_infos["name"]
            del material_infos["type"]

            self.database.update_material(
                self.item["id"], self.item["name"], material_infos
            )

        self.init_texts()"""
