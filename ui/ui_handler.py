"""
Scripts for Handling main window
"""

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import (
    QMainWindow,
    QDialog,
    QTextEdit,
    QComboBox,
    QWidget,
    QListWidgetItem,
    QListWidget,
    QAbstractItemView,
    QListView,
    QGraphicsDropShadowEffect,
    QPushButton,
)
from ui.ui_setups.ui_manager_window import Ui_MainWindow
from ui.ui_dialogs import (
    ImportAssetDialog,
    ImportTextureDialog,
    CreateMaterialDialog,
    DialogTemplate,
)

from ui.ui_items import ItemWidget

from bdd.database_handler import DatabaseHandler


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.items_lw.horizontalScrollBar().setEnabled(False)
        self.ui.items_lw.setWrapping(True)
        self.ui.items_lw.setResizeMode(QListView.ResizeMode.Adjust)
        self.filter_type = {"Models": True, "Textures": True, "Materials": True}
        self.thumbnails_cache = {}

        self.init_shadow_buttons()
        self.init_buttons()
        self.show()
        self.init_database()

    def enable_hover_event(self, button: QPushButton) -> None:
        button.setAttribute(Qt.WA_Hover, True)
        button.installEventFilter(self)

    def init_shadow_buttons(self) -> None:
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(10)
        self.shadow_effect.setXOffset(0)
        self.shadow_effect.setYOffset(3)
        self.shadow_effect.setColor(QColor(0, 0, 0, 50))

        self.enable_hover_event(self.ui.asset_btn)
        self.enable_hover_event(self.ui.texture_btn)
        self.enable_hover_event(self.ui.material_btn)

    def init_buttons(self) -> None:
        self.ui.asset_btn.clicked.connect(self.import_asset_event)
        self.ui.texture_btn.clicked.connect(self.import_texture_event)
        self.ui.material_btn.clicked.connect(self.create_material_event)

        self.ui.search_te.textChanged.connect(self.refresh_items)
        self.ui.all_check.clicked.connect(lambda: self.update_filter(True))
        self.ui.models_check.clicked.connect(lambda: self.update_filter(False))
        self.ui.textures_check.clicked.connect(lambda: self.update_filter(False))
        self.ui.materials_check.clicked.connect(lambda: self.update_filter(False))

    def init_database(self) -> None:
        self.database_handler = DatabaseHandler("assets.db")
        self.refresh_items(updateItems=True)

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

    def import_asset_event(self) -> None:
        infos = self.show_dialog(ImportAssetDialog)
        self.import_asset(infos)

    def import_asset(self, asset_infos: dict) -> None:
        if asset_infos == {}:
            return

        asset_id = self.database_handler.add_asset(
            asset_infos["name"], asset_infos["path"]
        )

        if asset_infos["material_id"] is not None:
            if asset_infos["material_id"] > 0:
                self.database_handler.link_material(
                    asset_id,
                    asset_infos["material_id"],
                )
        self.refresh_items(updateItems=True)

    def import_texture_event(self) -> None:
        infos = self.show_dialog(ImportTextureDialog)
        self.import_texture(infos)

    def import_texture(self, texture_infos: dict) -> None:
        if texture_infos == {}:
            return

        self.database_handler.add_texture(texture_infos["name"], texture_infos["path"])
        self.refresh_items(updateItems=True)

    def create_material_event(self) -> None:
        infos = self.show_dialog(CreateMaterialDialog)
        self.create_material(infos)

    def create_material(self, material_infos: dict) -> None:
        if material_infos == {}:
            return
        map_dict = {
            "diffuse_id": None,
            "specular_id": None,
            "roughness_id": None,
            "metalness_id": None,
            "normal_id": None,
            "displacement_id": None,
        }

        for key in map_dict.keys():
            map_dict[key] = material_infos[key]

        self.database_handler.add_materials(material_infos["name"], map_dict)
        self.refresh_items(updateItems=True)

    def show_dialog(self, dialog_class: DialogTemplate) -> dict:
        dialog = dialog_class(self.database_handler, {}, self)
        dialog.exec()
        return dialog.all_infos

    def add_all_items(self) -> None:
        for item in self.items:
            if item["type"] == "Textures":
                if "texture_" + str(
                    item["id"]
                ) not in self.thumbnails_cache and not item["path"].endswith(".exr"):
                    tmp_item = ItemWidget(self, self.database_handler)
                    map = QPixmap(item["path"])
                    self.thumbnails_cache["texture_" + str(item["id"])] = (
                        map.scaledToWidth(tmp_item.frameGeometry().width())
                    )
            item_widget = ItemWidget(
                self, self.database_handler, item, self.thumbnails_cache
            )
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

    def refresh_items(self, updateItems=True) -> None:
        if updateItems:
            self.items = self.get_all_items()
        self.ui.items_lw.clear()
        self.add_all_items()

    def get_file_name(self, path: str) -> str:
        last_slash = path[::-1].find("/")
        last_point = path[::-1].find(".")
        file_name = path[-last_slash : -last_point - 1]
        return file_name

    def get_file_extension(self, path: str) -> str:
        extension_index = path[::-1].find(".")
        return path[-extension_index - 1 :]

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        model_type = [".fbx", ".obj", ".abc"]
        texture_type = [".exr", ".jpg", ".png", ".tif", ".tiff"]

        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:  # Import Directly to database without opening popup
            extension = self.get_file_extension(f)
            file_name = self.get_file_name(f)
            if extension in model_type:
                self.database_handler.add_asset(file_name, f)
                continue
            if extension in texture_type:
                self.database_handler.add_texture(file_name, f)
                continue

        self.refresh_items()

    def eventFilter(self, source, event):
        if (
            source == self.ui.asset_btn
            or source == self.ui.texture_btn
            or source == self.ui.material_btn
        ):
            if event.type() == QEvent.Enter:
                source.setGraphicsEffect(self.shadow_effect)
                source.raise_()
                source.graphicsEffect().setEnabled(True)
            elif event.type() == QEvent.Leave:
                source.graphicsEffect().setEnabled(False)
        return super().eventFilter(source, event)
