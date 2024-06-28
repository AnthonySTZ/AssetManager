"""
Scripts for Handling all UI elements
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QDialog,
    QTextEdit,
    QComboBox,
    QWidget,
    QListWidgetItem,
    QListWidget,
    QAbstractItemView,
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
        self.filter_type = {"Models": True, "Textures": True, "Materials": True}

        self.init_buttons()
        self.show()
        self.init_database()

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

    def add_item_to_listWidget(self, list_widget, widget) -> None:
        item = QListWidgetItem(list_widget)
        item.setSizeHint(widget.size())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, widget)

    def add_item_row(self, item) -> None:
        list_widget = QListWidget()
        list_widget.setFlow(QListWidget.LeftToRight)
        list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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

    def refresh_items(self, updateItems=True) -> None:
        if updateItems:
            self.items = self.get_all_items()
        self.ui.items_lw.clear()
        self.add_all_items()

    def resizeEvent(self, event) -> None:
        QMainWindow.resizeEvent(self, event)
        try:  # Check if resize is called before the window is created
            self.refresh_items()
        except AttributeError:
            pass
