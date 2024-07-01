from PySide6.QtWidgets import (
    QWidget,
    QTextEdit,
    QComboBox,
    QGraphicsDropShadowEffect,
    QLabel,
    QStackedWidget,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import QEvent, QPropertyAnimation, QEasingCurve, Qt
from ui.ui_setups.ui_item_widget import Ui_Form as UiItemWidget
from ui.ui_dialogs import (
    ImportAssetDialog,
    ImportTextureDialog,
    CreateMaterialDialog,
    DialogTemplate,
)
from bdd.database_handler import DatabaseHandler
import os
import ressources_rc
import PySide6


class ItemWidget(QWidget):
    def __init__(
        self, parentDialog, database: DatabaseHandler, item=None, thumbnails_cache={}
    ) -> None:
        super().__init__()
        self.ui = UiItemWidget()
        self.ui.setupUi(self)
        self.database = database
        self.parentDialog = parentDialog
        self.thumbnails_cache = thumbnails_cache

        self.item = item
        self.init_texts()
        self.set_shadow()

    def set_shadow(self) -> None:
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setXOffset(0)
        effect.setYOffset(5)
        effect.setColor(QColor(0, 0, 0, 80))
        self.ui.frame.setGraphicsEffect(effect)
        self.ui.frame.raise_()
        self.ui.frame.graphicsEffect().setEnabled(False)

    def init_texts(self) -> None:
        if self.item is None:
            return
        self.ui.name_l.setText(self.item["name"])

        self.init_type()

    def init_type(self) -> None:
        if self.item["type"] == "Models":
            # self.ui.type_l.setStyleSheet("background-color: rgb(100, 0, 0);")
            self.set_icon("model")
        elif self.item["type"] == "Materials":
            # self.ui.type_l.setStyleSheet("background-color: rgb(0, 100, 0);")
            self.set_icon("material")
        else:
            # self.ui.type_l.setStyleSheet("background-color: rgb(0, 0, 100);")
            self.set_icon("texture")

    def set_icon(self, icon_name) -> None:
        icon = QPixmap(f":/icons/ui/ressources/{icon_name}")
        if "path" in self.item:
            if not os.path.exists(self.item["path"]):
                icon = QPixmap(":/icons/ui/ressources/error.png")
                self.ui.img_l.setPixmap(icon)
            else:
                if self.item["type"] == "Textures" and not self.item["path"].endswith(
                    ".exr"
                ):
                    icon = self.thumbnails_cache["texture_" + str(self.item["id"])]
                else:
                    icon = QPixmap(f":/icons/ui/ressources/{icon_name}")
        self.ui.img_l.setPixmap(icon)

    def enterEvent(self, event):
        self.ui.frame.graphicsEffect().setEnabled(True)

    def leaveEvent(self, event):
        self.ui.frame.graphicsEffect().setEnabled(False)

    def mouseReleaseEvent(self, event) -> None:
        if self.item is None:
            return

        if self.item["type"] == "Models":
            asset_infos = self.show_dialog(ImportAssetDialog, self.item)
            if asset_infos == {}:
                self.parentDialog.refresh_items()
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
                self.parentDialog.refresh_items()
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
                self.parentDialog.refresh_items()
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

        self.parentDialog.refresh_items()

        self.init_texts()

    def show_dialog(self, dialog_class: DialogTemplate, item) -> dict:
        dialog = dialog_class(self.database, item, self)
        dialog.exec()
        return dialog.all_infos
