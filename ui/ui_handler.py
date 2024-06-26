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

        self.init_buttons()
        self.show()
        self.init_database()

    def init_buttons(self) -> None:
        self.ui.asset_btn.clicked.connect(self.import_asset_event)
        self.ui.texture_btn.clicked.connect(self.import_texture_event)
        self.ui.material_btn.clicked.connect(self.create_material_event)

    def init_database(self) -> None:
        self.database_handler = DatabaseHandler("assets.db")
        self.refresh_items(updateItems=True)

    def closeEvent(self, event) -> None:
        self.database_handler.close_connection()

    def import_asset_event(self) -> None:
        infos = self.show_dialog(ImportAssetDialog)
        self.import_asset(infos)

    def import_asset(self, asset_infos: dict) -> None:
        if asset_infos == {}:
            return

        asset_id = self.database_handler.add_asset(
            asset_infos["name_te"], asset_infos["path_te"]
        )
        material_number = asset_infos["material_cb"]
        if material_number > 0:
            materials = self.database_handler.get_all_item_of_table("Materials")
            self.database_handler.link_material(
                asset_id,
                materials[material_number - 1]["id"],
            )
        self.refresh_items(updateItems=True)

    def import_texture_event(self) -> None:
        infos = self.show_dialog(ImportTextureDialog)
        self.import_texture(infos)

    def import_texture(self, texture_infos: dict) -> None:
        if texture_infos == {}:
            return

        self.database_handler.add_texture(
            texture_infos["name_te"], texture_infos["path_te"]
        )
        self.refresh_items(updateItems=True)

    def create_material_event(self) -> None:
        infos = self.show_dialog(CreateMaterialDialog)
        self.create_material(infos)

    def create_material(self, material_infos: dict) -> None:
        if material_infos == {}:
            return
        textures = self.database_handler.get_all_item_of_table("Textures")
        map_dict = {
            "diffuse_id": None,
            "specular_id": None,
            "roughness_id": None,
            "metalness_id": None,
            "normal_id": None,
            "displacement_id": None,
        }
        dict_texture_name = {
            "diffuse_cb": "diffuse_id",
            "specular_cb": "specular_id",
            "roughness_cb": "roughness_id",
            "metalness_cb": "metalness_id",
            "normal_cb": "normal_id",
            "displacement_cb": "displacement_id",
        }

        for input_name, texture_name in dict_texture_name.items():
            texture_number = material_infos[input_name]
            if texture_number > 0:
                map_dict[texture_name] = textures[texture_number - 1]["id"]

        self.database_handler.add_materials(material_infos["name_te"], map_dict)
        self.refresh_items(updateItems=True)

    def show_dialog(self, dialog_class: DialogTemplate) -> dict:
        dialog = dialog_class(self.database_handler, self)
        dialog.exec()
        if dialog.status != True:  # Return Empty dict if Dialog cancel or close
            return {}

        objects_dict = {}
        labels = dialog.findChildren(QTextEdit)
        for obj in labels:
            objects_dict[obj.objectName()] = obj.toPlainText()

        comboboxes = dialog.findChildren(QComboBox)
        for obj in comboboxes:
            objects_dict[obj.objectName()] = obj.currentIndex()

        return objects_dict

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
        list_widget.setFixedSize(self.ui.items_lw.width(), ItemWidget().height() + 10)
        self.add_item_to_listWidget(self.ui.items_lw, list_widget)

    def is_item_row_full(self):

        last_row_item = self.ui.items_lw.item(self.ui.items_lw.count() - 1)
        last_row = self.ui.items_lw.itemWidget(last_row_item)
        last_row_item_nb = last_row.count()
        widget_width = ItemWidget().width()
        return (last_row_item_nb + 1) * widget_width > self.ui.items_lw.width()

    def add_item(self, item) -> None:
        if self.ui.items_lw.count() == 0:
            self.add_item_row(item)

        elif self.is_item_row_full():
            self.add_item_row(item)

        item_widget = ItemWidget(item)
        last_row_item = self.ui.items_lw.item(self.ui.items_lw.count() - 1)
        self.add_item_to_listWidget(
            self.ui.items_lw.itemWidget(last_row_item), item_widget
        )

    def add_all_items(self) -> None:
        for item in self.items:
            self.add_item(item)

    def get_all_items(self) -> list[dict]:
        self.all_assets = self.database_handler.get_all_item_of_table("Models")
        self.all_textures = self.database_handler.get_all_item_of_table("Textures")
        self.all_materials = self.database_handler.get_all_item_of_table("Materials")

        return self.all_assets + self.all_textures + self.all_materials

    def refresh_items(self, updateItems: bool) -> None:
        if updateItems:
            self.items = self.get_all_items()
        self.ui.items_lw.clear()
        self.add_all_items()

    def resizeEvent(self, event) -> None:
        QMainWindow.resizeEvent(self, event)
        try:  # Check if resize is called before the window is created
            self.refresh_items(updateItems=False)
        except AttributeError:
            pass
